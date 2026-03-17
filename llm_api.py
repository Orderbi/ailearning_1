import requests
import time
from config import API_URL, API_KEY, MODEL_NAME

"""
只负责大模型调用，以后要换模型，只需要改这个文件
"""


def call_llm(system_prompt, user_content, retry_time=3):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        "temperature": 0.1,
        "max_tokens": 2048
    }

    for i in range(retry_time):
        try:
            response = requests.post(API_URL, headers=headers, json=body, timeout=60)
            response.raise_for_status()
            # 将返回的JSON格式内容解析为python中的对象
            response_json = response.json()
            answer = response_json["choices"][0]["message"]["content"]
            return answer
        except Exception as e:
            print(f"第{i + 1}次调用失败，失败原因为{str(e)}")
            # 最后一次调用仍然失败时给个信息提示
            if i == retry_time - 1:
                print("你已经失败了多次，请检查api密钥或者网络问题")
                return None
            # 重试前休眠一秒，避免频繁请求
            time.sleep(1)
