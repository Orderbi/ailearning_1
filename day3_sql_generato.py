# 导入所需要的库
import requests  # 用来发送请求，调用API
import os  # 用来读取系统环境变量
from dotenv import load_dotenv  # 用来读取.env文件中的密钥

"""
写专属 SQL 生成 Prompt，把 SQL 生成逻辑封装成独立函数，输入自然语言需求，
直接返回可用的 SQL，把函数封装、字符串格式化、条件判断知识点落地

【运行步骤】
1. 替换 MODEL_NAME 后运行脚本，控制台会直接输出生成的 SQL 代码
2. 练习 1：修改 my_requirement 成你工作里的真实需求，重新运行，看生成的 SQL 是否能用
3. 练习 2：修改 sql_type 为 Hive，测试生成 Hive 语法的 SQL
【抄写 & 学习重点】
1. 重点理解「Prompt 工程」的核心：通过系统提示词，给大模型设定角色、规则、约束，让它精准输出你想要的内容
2. 理解函数的入参和出参：generate_sql 函数接收 2 个入参（需求、语法类型），返回 1 个结果（SQL 代码）
3. 理解为什么 temperature 设成 0.1：SQL 生成需要固定、准确的结果，不需要创意性
4. 练习修改 Prompt 里的规则，比如加上「生成的 SQL 必须加上字段注释」，看结果变化
"""
# 加载密钥，不放在代码里，更安全
load_dotenv()
API_KEY = os.getenv("DP_SK_API_KEY")
# 固定的api配置，deepseek的官网接口地址
API_URL = "https://api.deepseek.com/chat/completions"
# 选用模型
MODEL_NAME = "deepseek-chat"


# 1.封装通用的大模型调用函数，与day2的逻辑基本一致，以后可以重复调用
def call_llm(system_prompt, user_content):
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
    # 发送post请求，调用API
    response = requests.post(url=API_URL, headers=headers, json=body)
    # 把返回的结果转换为python能处理的字典格式
    response_json = response.json()
    # 提取大模型返回的纯文本内容
    answer = response_json["choices"][0]["message"]["content"]
    return answer


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


# 3. 封装SQL生成函数，输入自然语言需求，直接返回SQL
def generate_sql(user_requirement, sql_type="hive-sql"):
    # 把用户指定的语法类拼到SQL里
    final_prompt = SQL_GENERATOR_PROMPT.replace("默认使用Hive SQL语法", f"默认使用{sql_type}语法")
    # 调用大模型，拿到生成的SQL
    sql_result = call_llm(final_prompt, user_requirement)
    return sql_result


if __name__ == '__main__':
    my_requirement1 = "查询user表中，2024年1月1日之后注册的男性用户总数，用户性别字段是gender，注册时间字段是register_time"
    final_sql1 = generate_sql(my_requirement1, sql_type="mysql")
    final_sql2 = generate_sql(my_requirement1,)
    print(f"最终生成的SQL：\n {final_sql1}")
    print(f"最终生成的SQL：\n {final_sql2}")
