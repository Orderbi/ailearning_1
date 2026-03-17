# 导入所需要的库
import time

import requests  # 用来发送请求，调用API
import os  # 用来读取系统环境变量
from dotenv import load_dotenv  # 用来读取.env文件中的密钥

"""
【运行步骤】
替换 MODEL_NAME 后运行脚本，测试正常情况的 SQL 生成
练习 1：故意把 API 密钥改错，运行脚本，看异常处理的效果，会不会直接崩溃
练习 2：把需求改成「今天天气怎么样」，运行脚本，看 SQL 校验的效果
【抄写 & 学习重点】
重点理解 try-except 异常处理的作用：捕获代码运行中的错误，不让脚本直接崩溃，同时给出错误提示，方便排查
理解重试机制的意义：网络波动是常有的事，自动重试能大幅提升脚本的可用性
理解 check_sql_valid 函数的逻辑：通过关键字匹配，过滤掉大模型返回的无效内容，保证输出的是 SQL
理解 if not xxx 的判空逻辑，这是 Python 里最常用的校验写法
"""
# 加载密钥，不放在代码里，更安全
load_dotenv()
API_KEY = os.getenv("DP_SK_API_KEY")
# 固定的api配置，deepseek的官网接口地址
API_URL = "https://api.deepseek.com/chat/completions"
# 选用模型
MODEL_NAME = "deepseek-chat"


# 1.升级大模型调用函数：加异常处理+超时重试
def call_llm(system_prompt, user_content, retry_times=3):
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
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        "temperature": 0.1,  # 数值越小回答越稳定，越大回答越随机
        "max_tokens": 1024  # 限制大模型返回的最大长度
    }
    for i in range(retry_times):
        try:
            # 发送post请求，调用API
            response = requests.post(url=API_URL, headers=headers, json=body, timeout=60)
            # 检查请求是否成功，状态码200才算是成功
            response.raise_for_status()
            response_json = response.json()  # 把返回的结果转换为python能处理的字典格式
            answer = response_json["choices"][0]["message"]["content"]  # 提取大模型返回的纯文本内容
            return answer
        except Exception as e:
            # 捕获异常，打印错误信息，不会直接崩溃
            print(f"第{i + 1}次调用API失败，返回None")
            if i == retry_times - 1:
                print("API调用多次失败，请检查网络或者API密钥")
                return None
            # 重试前等待1秒，避免频繁请求
            time.sleep(1)


# 2.写专属的SQL生成系统prompt，是生成SQL的核心
SQL_GENERATOR_PROMPT = """
你是一名拥有10年经验的资深Hive/MySQL SQL开发工程师，你的唯一任务是生成符合要求的、可直接运行的SQL代码。
请严格遵守以下规则：
1.  只输出纯SQL代码，不要输出任何解释、说明、备注、问候语，不要用```包裹代码
2.  严格按照用户指定的数据库语法生成SQL，默认使用Hive SQL语法
3.  生成的SQL要规范、简洁，字段名、表名要和用户需求里的一致
4.  禁止生成任何和SQL无关的内容，哪怕用户问的问题和SQL无关，也只返回「请输入有效的SQL生成需求」
5.生成的sql必须加上注释
6、造点测试数据并输出结果
"""


# 3.新增：SQL校验函数，判断返回的内容是不是有效的SQL
def check_sql_valid(sql_content):
    # 3.1 如果是None或者空字符串直接返回False
    if not sql_content:
        return False
    # 3.2 如果传入的内容非空，才有走下一步：校验SQL是否包含关键字
    # 定义SQL核心关键字，只有包含这些关键字，才认为是有效的SQL
    sql_keywords = ["SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "JOIN", "GROUP BY", "ORDER BY"]
    # 把内容转成大写，避免大小写问题
    sql_upper = sql_content.upper()
    # 检查否包含至少一个核心关键字：如果关键词列表很长，这种短路行为可以节省时间
    for keyword in sql_keywords:
        if keyword in sql_upper:
            # 如果是合法的SQL则直接返回TRUE
            return True
    # 整个循环完，都没找到关键字，判定为无效SQL
    return False


# 4. 升级SQL生成函数：加校验逻辑
def generate_sql(user_requirement, sql_type="hive-sql"):
    # 把用户指定的语法类拼到SQL里
    final_prompt = SQL_GENERATOR_PROMPT.replace("默认使用Hive SQL语法", f"默认使用{sql_type}语法")
    # 调用大模型，拿到生成的SQL
    sql_result = call_llm(final_prompt, user_requirement)
    # 检验生成的SQL是否有效
    if not check_sql_valid(sql_result):
        print("生成的内容不是有效SQL，请重新描述你的需求")
        return None
    return sql_result


# 5.主程序，测试功能
if __name__ == '__main__':
    my_requirement = "今天天气怎么样"
    # my_requirement = "查询user表中，2024年1月1日之后注册的男性用户总数，用户性别字段是gender，注册时间字段是register_time"
    final_sql = generate_sql(my_requirement, sql_type="mysql")

    # 只有生成了有效的SQL才打印
    if final_sql:
        print(f"生成的有效的SQL代码：\n {final_sql}")
