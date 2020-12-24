import os
import HTMLTestRunner
import unittest
from config import config
from datetime import datetime

load = unittest.TestLoader()
suit = load.discover(config.CASE_PATH)

# 测试报告路径
report_name = "report-{}.html".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
report_file_path = os.path.join(config.REPORT_PATH, report_name)

with open(report_file_path, "wb") as f:
    runner = HTMLTestRunner.HTMLTestRunner(stream=f, title="前程贷接口测试报告",
                                           description='接口自动化测试')
    runner.run(suit)
