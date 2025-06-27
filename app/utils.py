from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def init_model(model_name="deepseek-ai/deepseek-llm-7b-chat", device=None):
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=torch.float16 if device=="cuda" else torch.float32
    )
    model = model.to(device).eval()
    model.generation_config.pad_token_id = tokenizer.eos_token_id
    return tokenizer, model, device

def safe_chat(tokenizer, model, prompt, max_tokens=1024, temperature=0.7):
    try:
        full_prompt = f"<|system|>\n你是一个专业问答助手。\n<|user|>\n{prompt}\n<|assistant|>\n"
        inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=False
            )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        if "<|assistant|>" in response:
            response = response.split("<|assistant|>")[-1].strip()
        return response
    except Exception as e:
        print(f"⚠️ 推理失败: {e}")
        return None 