from transformers import AutoModelForCausalLM, AutoTokenizer
from .config import DEEPSEEK_MODEL_PATH

# 初始化模型（全局只加载一次）
tokenizer = AutoTokenizer.from_pretrained(DEEPSEEK_MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(DEEPSEEK_MODEL_PATH)

def generate_questions(content):
    """
    用DeepSeek模型为content生成两个问题，返回问题列表
    """
    prompt = f"请为以下内容生成两个常见问题：\n"{content}"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=128)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 简单分割提取两个问题
    questions = [q.strip() for q in result.split('\n') if q.strip()]
    return questions[:2] 