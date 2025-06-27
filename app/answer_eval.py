import requests
import re
from .utils import init_model, safe_chat
from .config import DIFY_API_URL, DIFY_API_KEY

tokenizer, model, device = init_model()

def get_ai_answer_and_judge(question, content):
    """
    1. 用Dify API回答问题
    2. 用DeepSeek判定回答是否正确
    返回(ai_answer, is_correct)
    """
    # 1. Dify问答
    headers = {"Authorization": f"Bearer {DIFY_API_KEY}"}
    data = {
        "inputs": {"question": question},
        "query": question,
        "response_mode": "blocking"
    }
    resp = requests.post(DIFY_API_URL, headers=headers, json=data, timeout=60)
    ai_answer = resp.json().get("answer", "")

    # 2. DeepSeek判定
    judge_prompt = (
        f"请判断下面的AI回答是否包含或正确表达了原始内容。\n"
        f"问题：{question}\n"
        f"原文内容：{content}\n"
        f"AI回答：{ai_answer}\n"
        f"请仅输出"正确"或"错误""
    )
    response = safe_chat(tokenizer, model, judge_prompt, max_tokens=16)
    if not response:
        return ai_answer, "错误"
    match = re.search(r"(正确|错误)", response)
    is_correct = match.group(1) if match else "错误"
    return ai_answer, is_correct 