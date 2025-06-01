
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
API_URL = "https://chat.intern-ai.org.cn/api/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

data = {
    "model": "internlm3-latest",
    "messages": [
        {"role": "user", "content": "你好，请说一句英语。"}
    ],
    "temperature": 0.7
}

response = requests.post(API_URL, headers=headers, json=data)
print(response.status_code)
print(response.text)
