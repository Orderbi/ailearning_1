from llm_api import call_llm
from config import SQL_GENERATOR_PROMPT, SQL_OPTIMIZER_PROMPT, SQL_EXPLAINER_PROMPT, SQL_FORMATTED_PROMPT

"""
只负责业务功能逻辑，新增功能，只需要改这个文件
"""


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


# 4.1 SQL生成函数
def generate_sql(user_requirement, sql_type="hive"):
    final_prompt = SQL_GENERATOR_PROMPT.replace("默认使用Hive SQL语法", f"默认使用{sql_type} SQL语法")
    sql_result = call_llm(final_prompt, user_requirement)
    if not check_sql_valid(sql_result):
        print("生成的不是有效的SQL，请重新描述你的需求")
        return None
    return sql_result


def optimize_sql(raw_sql, sql_type="Hive"):
    user_content = f"我使用的是{sql_type}数据库，请优化下面的sql代码" \
                   f"：\n{raw_sql}"
    optimize_result = call_llm(SQL_OPTIMIZER_PROMPT, user_content)
    return optimize_result


def explain_sql(raw_sql):
    explain_result = call_llm(SQL_EXPLAINER_PROMPT, raw_sql)
    return explain_result


def formatted_sql(raw_sql):
    formatted_sql = call_llm(SQL_FORMATTED_PROMPT, raw_sql)
    return formatted_sql
