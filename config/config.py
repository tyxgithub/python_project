import os

# 配置文件路径
CON_PATH = os.path.dirname(os.path.abspath(__file__))

# 项目路径
ROOT_PATH = os.path.dirname(CON_PATH)

# 测试用例路径
CASE_PATH = os.path.join(ROOT_PATH, "testCases")

# 测试报告路径
REPORT_PATH = os.path.join(ROOT_PATH, "report")

# excel路径
EXCEL_PATH = os.path.join(ROOT_PATH, 'data')

# log_path日志路径
LOGGER_PATH = os.path.join(ROOT_PATH, 'logs')

if __name__ == '__main__':
    print("配置文件路径：%s" % CON_PATH)
    print("项目路径: %s" % ROOT_PATH)
    print("测试用例路径: %s" % CASE_PATH)
    print("测试报告路径: %s" % REPORT_PATH)
    print("EXCEL数据文件路径: %s" % EXCEL_PATH)
    print("日志文件路径: %s" % LOGGER_PATH)
