from sql_utils import generate_sql, optimize_sql, explain_sql,formatted_sql
from menu import print_menu
# 只负责用户交互，界面修改
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
            sql_type = input("请输入数据库类型（Hive/MySQL，默认Hive）：") or "Hive"
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
        elif choice == "4":
            print("\n--- SQL格式化 ---")
            raw_sql = input("请输入你要格式化的SQL代码：")
            print("\n 正在格式化SQL，请稍候...")
            result = formatted_sql(raw_sql)
            if result:
                print("\n sql格式化完成，格式化后的结果如下：")
                print(result)
        elif choice == "0":
            print("\n 感谢使用 工具已退出")
            break

        else:
            print("\n 输入错误，请输入0-3之间的数字")
