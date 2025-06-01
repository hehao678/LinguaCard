import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
API_URL = "https://chat.intern-ai.org.cn/api/v1/chat/completions"
MODEL_NAME = "internlm3-latest"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}


def generate_image_prompt_by_llm(data: dict) -> str:
    zhuti = data.get("zhuti", "未知主题")
    title_en = data.get("zhutien", "")
    desc_en = data.get("zhengwen", "")

    system_prompt = "你是一个插画师，擅长设计英文提示词用于生成插图。风格偏卡通、油画、色彩明亮，符合儿童学习主题。"
    user_prompt = f"""
请根据以下学习卡片内容，输出一个用于插图生成的英文提示词（英文描述即可，不要添加其他解释性文字）：

【主题】：{zhuti}
【英文标题】：{title_en}
【英文描述】：{desc_en}
    """

    body = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.8,
        "top_p": 0.9,
        "max_tokens": 256
    }

    try:
        response = requests.post(API_URL, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"[ERROR] 插图提示词生成失败：{e}")
        return f"cartoon oil painting of {zhuti}, colorful, bright, cheerful"


if __name__ == "__main__":
    example = {
        "zhuti": "美食",
        "zhutien": "Exploring Delicious Cuisine",
        "zhengwen": "Welcome to the world of food! This card is your guide to discovering the delights of various cuisines..."
    }
    print(generate_image_prompt_by_llm(example))
