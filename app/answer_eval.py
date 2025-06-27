import requests
from transformers import AutoModelForCausalLM, AutoTokenizer
from .config import DIFY_API_URL, DIFY_API_KEY, DEEPSEEK_MODEL_PATH

# DeepSeek模型用于判定
tokenizer = AutoTokenizer.from_pretrained(DEEPSEEK_MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(DEEPSEEK_MODEL_PATH)

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
        f"请仅输出'正确'或'错误'"
    )
    inputs = tokenizer(judge_prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=16)
    judge_result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 只保留"正确"或"错误"
    is_correct = "正确" if "正确" in judge_result else "错误"
    return ai_answer, is_correct 