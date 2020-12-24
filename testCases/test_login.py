import unittest
import ddt
from config import config
import os
from common.request_handler import *
from middleware import middle_handler
import json

logger = middle_handler.Handler.logger
test_data = middle_handler.Handler.excel.read_data("login")


@ddt.ddt
class TestLogin(unittest.TestCase):
    @ddt.data(*test_data)
    def test_login(self, test_info):
        id = test_info["case_id"]
        res = visit(url=middle_handler.Handler.yaml["host"] + test_info["url"],
                    method=test_info["method"],
                    json=json.loads(test_info["data"]),
                    headers=json.loads(test_info["headers"]))
        try:
            for key, value in json.loads(test_info["expected"]).items():
                self.assertTrue(value == res[key])
            middle_handler.Handler.logger.info("测试用例:{}通过".format((test_info["case_id"])))
        except AssertionError as e:
            middle_handler.Handler.excel.write(row=id + 1, column=9, data="不通过", sheet="login")
            middle_handler.Handler.logger.info("测试用例{}：{},执行成功".format(test_info["case_id"], test_info["title"]))
            middle_handler.Handler.logger.error(e)
            raise e
        else:
            middle_handler.Handler.logger.info("测试用例{}：{},执行成功".format(test_info["case_id"], test_info["title"]))
            middle_handler.Handler.excel.write(row=id + 1, column=9, data="通过", sheet="login")


if __name__ == '__main__':
    unittest.main()
