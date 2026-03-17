import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()  # 把.env文件中的内容添加到系统环境变量中
API_KEY = os.getenv("DP_SK_API_KEY")  # 加载API密钥
API_URL = "https://api.deepseek.com/chat/completions"  # 固定的api配置，deepseek的官网接口地址
MODEL_NAME = "deepseek-chat"  # 选用模型


# 1.通用大模型调用函数
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


# 2. 三个核心功能的专属Prompt
# 2.1 SQL生成Prompt
SQL_GENERATOR_PROMPT = """
你是一名拥有10年经验的资深Hive/MySQL SQL开发工程师，你的唯一任务是生成符合要求的、可直接运行的SQL代码。
请严格遵守以下规则：
1.  只输出纯SQL代码，不要输出任何解释、说明、备注、问候语，不要用```包裹代码
2.  严格按照用户指定的数据库语法生成SQL，默认使用Hive SQL语法
3.  生成的SQL要规范、简洁，字段名、表名要和用户需求里的一致
4.  禁止生成任何和SQL无关的内容，哪怕用户问的问题和SQL无关，也只返回「请输入有效的SQL生成需求」
"""
# 2.2 新增：SQL优化Prompt
SQL_OPTIMIZER_PROMPT = """
你是一名拥有10年经验的资深SQL性能优化专家，擅长Hive/MySQL SQL优化。
你的任务是对用户输入的SQL进行性能优化，同时保证逻辑完全不变，输出优化后的SQL和优化原因。
请严格遵守以下规则：
1.  先输出优化后的完整SQL代码，再输出优化原因，分点说明
2.  优化要贴合对应数据库的特性，比如Hive要优化分区裁剪、数据倾斜，MySQL要优化索引、执行计划
3.  不要改变原SQL的业务逻辑，保证优化前后的查询结果完全一致
4.  语言要简洁专业，通俗易懂，不要说废话
"""

# 2.3 新增：SQL解释Prompt
SQL_EXPLAINER_PROMPT = """
你是一名拥有10年经验的资深SQL讲师，擅长给新手解释SQL代码的逻辑。
你的任务是逐行解释用户输入的SQL代码，讲清楚每一段的作用、整体的业务逻辑。
请严格遵守以下规则：
1.  先说明SQL的整体业务用途，再逐行/逐段解释代码逻辑
2.  语言要通俗易懂，不要用太专业的黑话，新手能看懂
3.  结构清晰，分点说明，不要杂乱无章
"""


# 3. SQL校验函数，和Day4一致，直接复用
def check_sql_valid(sql_content):
    # 判断输入内容是否为空，是空的话直接返回False，退出当前函数
    if not sql_content:
        return False
    # 如果输入内容不为空，再判断是否为有效的SQL语句
    sql_keywords = ["SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "JOIN", "GROUP BY", "ORDER BY"]
    sql_upper = sql_content.upper()
    for key_word in sql_keywords:
        if key_word in sql_upper:
            return True
    # 都不包含才返回false
    return False


# 4. 三个核心功能函数
# 4.1 SQL生成函数
def generate_sql(user_requirement, sql_type="hive"):
    final_prompt = SQL_GENERATOR_PROMPT.replace("默认使用Hive SQL语法", f"默认使用{sql_type} SQL语法")
    sql_result = call_llm(final_prompt, user_requirement)
    if not check_sql_valid(sql_result):
        print("生成的不是有效的SQL，请重新描述你的需求")
        return None
    return sql_result


# 4.2 新增：SQL优化函数
def optimize_sql(raw_sql, sql_type="Hive"):
    user_content = f"我使用的是{sql_type}数据库，请优化下面的sql代码" \
                   f"：\n{raw_sql}"
    optimize_result = call_llm(SQL_OPTIMIZER_PROMPT, user_content)
    return optimize_result


# 4.3 新增：SQL解释函数
def explain_sql(raw_sql):
    explain_result = call_llm(SQL_EXPLAINER_PROMPT, raw_sql)
    return explain_result
# 主循环中的菜单打印可以提取为一个函数，使主逻辑更清晰
def print_menu():
    print("\n请选择你要使用的功能：")
    print("1. 自然语言生成SQL")
    print("2. SQL性能优化")
    print("3. SQL逻辑解释")
    print("0. 退出工具")

if __name__ == '__main__':
    print("=" * 50)
    print("欢迎使用SQL智能助手工具")
    print("=" * 50)
    while True:
        # 打印菜单功能
        print_menu()
        # 获取用户的选择
        choice = input("\n 请输入对应的数字：").strip()
        if choice == "1":
            print("\n--- 自然语言生成SQL ---")
            requirement = input("请输入你的SQL需求：")
            sql_type = input("请输入数据库类型（Hive/MySQL，默认Hive）：" ) or "Hive"
            print("正在生成SQL，请稍后...")
            result = generate_sql(requirement, sql_type)
            if result:
                print("\n? 生成完成，结果如下：")
                print(result)
        elif choice == "2":
            raw_sql = input("请输入你要优化的SQL代码：")
            sql_type = input("请输入数据库类型（Hive/MySQL，默认Hive）：") or "Hive"
            print("正在优化SQL，请稍候...")
            result = optimize_sql(raw_sql, sql_type)
            if result:
                print("\n? 优化完成，结果如下：")
                print(result)
        elif choice == "3":
            print("\n--- SQL逻辑解释 ---")
            raw_sql = input("请输入你要解释的SQL代码：")
            print("正在解释SQL，请稍候...")
            result = explain_sql(raw_sql)
            if result:
                print("\n? 解释完成，结果如下：")
                print(result)
        elif choice == "0":
            print("\n 感谢使用 工具已退出")
            break

        else:
            print("\n 输入错误，请输入0-3之间的数字")
