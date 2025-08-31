import torch
from llama_index.core import Settings
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


LLM_MODEL_PATH = "/media/sdb1/sjx/Qwen2.5-7B-Instruct"
EMBED_MODEL_PATH = "/media/sdb1/sjx/bge-base-en-v1.5"
JSON_DATA_PATH = "/media/sdb1/sjx/ragMinecraft/minecraft_qa.json"
INDEX_SAVE_PATH = "/media/sdb1/sjx/ragMinecraft/saved_index" 

def messages_to_prompt(messages):
    prompt = ""
    for message in messages:
        if message.role == 'system':
            prompt += f"<|im_start|>system\n{message.content}<|im_end|>\n"
        elif message.role == 'user':
            prompt += f"<|im_start|>user\n{message.content}<|im_end|>\n"
        elif message.role == 'assistant':
            prompt += f"<|im_start|>assistant\n{message.content}<|im_end|>\n"
    if not prompt.endswith("<|im_start|>assistant\n"):
        prompt += "<|im_start|>assistant\n"
    return prompt

def completion_to_prompt(completion):
     return f"<|im_start|>assistant\n{completion}<|im_end|>\n"

def setup_models():
    print("开始配置模型...")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"检测到设备: {device}")
    
    Settings.llm = HuggingFaceLLM(
        model_name=LLM_MODEL_PATH,
        tokenizer_name=LLM_MODEL_PATH,
        context_window=8192,
        max_new_tokens=2048,
        generate_kwargs={"temperature": 0.2, "do_sample": True},
        messages_to_prompt=messages_to_prompt,
        completion_to_prompt=completion_to_prompt,
        device_map="auto",
        model_kwargs={"torch_dtype": torch.bfloat16}
    )

    Settings.embed_model = HuggingFaceEmbedding(
        model_name=EMBED_MODEL_PATH,
        cache_folder="/home/mcislab/.cache",
        device=device
    )
    print("模型配置完成！")
