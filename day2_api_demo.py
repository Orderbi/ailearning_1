"""
【运行步骤】
把代码里的 MODEL_NAME 替换成你自己在豆包平台创建的模型 endpoint_id
右键运行这个脚本，在控制台就能看到大模型的回答
练习：修改 my_question 里的内容，比如改成「Python 里的函数是什么？」，重新运行，看结果变化
【抄写 & 学习重点】
重点理解 call_llm 函数的作用：把重复的 API 调用逻辑封装起来，以后不用每次都写一遍
搞懂 headers 和 body 里每个参数的含义，特别是 messages 的对话结构
理解 temperature 参数的作用，改成 0.1 和 0.9 分别测试，看回答有什么区别
记住怎么从返回结果里提取纯文本，这是所有大模型应用的基础

"""

# 导入所需要的库
import requests  # 用来发送请求，调用API
import os  # 用来读取系统环境变量
from dotenv import load_dotenv  # 用来读取.env文件中的密钥

# 1.加载密钥，不放在代码里，更安全
load_dotenv()
API_KEY = os.getenv("DP_SK_API_KEY")

# 2.固定的api配置，deepseek的官网接口地址
API_URL = "https://api.deepseek.com/chat/completions"
# 选用模型
MODEL_NAME = "deepseek-chat"


# 3.定义一个调用大模型的函数，输入问题，返回大模型的回答
def call_llm(user_question):
    # 构造请求头，告诉api身份和数据格式
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        # 声明请求体的数据格式是JSON，告诉服务器该以什么方式解析请求的数据
        "Content-Type": "application/json"
    }
    # 构造请求体，告诉大模型要做什么
    body = {
        "model": MODEL_NAME,
        # message就是对话内容，role 分为system(系统提示)和user(用户输入)
        "messages": [
            {
                "role": "system",
                "content": "你是一个专业的助手，回答要简洁准确，不要说多余的废话"
            },
            {
                "role": "user",
                "content": user_question
            }
        ],
        "temperature": 0.3,  # 数值越小回答越稳定，越大回答越随机
        "max_tokens": 1024  # 限制大模型返回的最大长度
    }
    # 发送post请求，调用API
    response = requests.post(url=API_URL, headers=headers, json=body)
    # 把返回的结果转换为python能处理的字典格式
    response_json = response.json()
    # 提取大模型返回的纯文本内容
    answer = response_json["choices"][0]["message"]["content"]
    return answer


if __name__ == '__main__':
    # aws = call_llm("千禧之年的七大数学难题是什么？")
    # print(f"大模型的回答是：\n{aws}")
    print("11")
