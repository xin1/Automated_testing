from .utils import init_model, safe_chat

tokenizer, model, device = init_model()

def generate_questions(content):
    """
    用DeepSeek模型为content生成两个问题，返回问题列表
    """
    prompt = f"请为以下内容生成两个常见问题，每个问题单独一行：\n"{content}"
    response = safe_chat(tokenizer, model, prompt, max_tokens=128)
    if not response:
        return []
    questions = [q.strip() for q in response.split('\n') if q.strip()]
    return questions[:2] 