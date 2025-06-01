
import requests
import os
from dotenv import load_dotenv

# 加载 .env 中的 API_TOKEN
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
API_URL = "https://chat.intern-ai.org.cn/api/v1/chat/completions"
MODEL_NAME = "internlm3-latest"


def generate_card_content(topic="美食", level="小学", word_count=60):
    """
    调用 InternLM 模型生成英语学习卡片内容
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    prompt = f"""
    你是一个英语教学助手，请帮助生成一张英语学习卡片内容，务必按照如下格式严格输出：

    【中文标题】：...
    【英文标题】：...
    【英文描述】：...
    【中文翻译】：...
    【重点词汇】：
    - word (/音标/): 中文含义
    ...
    【普通词汇】：
    - word (/音标/): 中文含义
    ...

    要求如下：
    - 主题：{topic}
    - 阶段：{level}
    - 描述英文单词不少于 {word_count} 个
    - 所有输出请使用 UTF-8 编码
    """

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        print("[DEBUG] 返回内容：", result)

        if "choices" not in result:
            raise ValueError("API 响应不包含 'choices' 字段")

        reply = result['choices'][0]['message']['content']
        return parse_card_output(reply)
    except Exception as e:
        print("[ERROR] 卡片生成失败：", e)
        return None


def parse_card_output(text):
    """
    将模型返回的卡片文本解析为结构化字段
    """
    from re import search
    output = {
        "zhuti": search(r"【中文标题】：(.+)", text).group(1).strip() if search(r"【中文标题】：(.+)", text) else "未命名",
        "zhutien": search(r"【英文标题】：(.+)", text).group(1).strip() if search(r"【英文标题】：(.+)", text) else "Untitled",
        "zhengwen": search(r"【英文描述】：(.+)", text).group(1).strip() if search(r"【英文描述】：(.+)", text) else "",
        "zhongwenfanyi": search(r"【中文翻译】：(.+)", text).group(1).strip() if search(r"【中文翻译】：(.+)", text) else "",
        "putong": "",
        "zhongdian": ""
    }

    # 简单解析词汇部分
    lines = text.splitlines()
    current = None
    for line in lines:
        if "【重点词汇】" in line:
            current = "zhongdian"
        elif "【普通词汇】" in line:
            current = "putong"
        elif line.strip().startswith("-"):
            if current:
                output[current] += line.strip() + "<br>"
    print(output)
    return output


if __name__ == "__main__":
    from pprint import pprint
    result = generate_card_content("美食", "小学", 60)
    pprint(result)
