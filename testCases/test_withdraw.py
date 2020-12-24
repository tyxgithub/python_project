import ddt
import unittest
import json
from middleware import middle_handler
from common import request_handler
from decimal import Decimal

# 初始化日志
logger = middle_handler.Handler.logger
# 初始化测试数据
test_data = middle_handler.Handler.excel.read_data("withdraw")


@ddt.ddt
class TestWithDraw(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.token = middle_handler.Handler().token
        cls.member_id = middle_handler.Handler().member_id

    def setUp(self) -> None:
        self.db = middle_handler.Handler.db_class()

    @ddt.data(*test_data)
    def test_withdraw(self, test_info):
        if "#token#" in test_info["headers"]:
            test_info["headers"] = test_info["headers"].replace("#token#", self.token)
        if "#member_id#" in test_info["data"]:
            test_info["data"] = test_info["data"].replace("#member_id#", str(self.member_id))
        if "#amount#" in test_info["data"]:
            leave_amount = \
                self.db.query("select leave_amount from futureloan.member where id={}".format(self.member_id))[
                    "leave_amount"]
            test_info["data"] = test_info["data"].replace("#amount#", str(leave_amount))
        before_amont = self.db.query("select leave_amount from futureloan.member where id={}".format(self.member_id))[
            "leave_amount"]
        res = request_handler.visit(method=test_info["method"],
                                    url=middle_handler.Handler.yaml["host"] + test_info["url"],
                                    json=json.loads(test_info["data"]),
                                    headers=json.loads(test_info["headers"]))
        try:
            if res == 0:
                after_mount = \
                    self.db.query("select leave_amount from futureloan.member where id={}".format(self.member_id))[
                        "leave_amount"]
                self.assertTrue(before_amont - Decimal(str(json.loads(test_info["data"])["amount"])) == after_mount)
            if res != 0:
                for key, value in json.loads(test_info["expected"]).items():
                    self.assertTrue(res[key] == value)
        except Exception as e:
            middle_handler.Handler.excel.write(row=1 + test_info["case_id"], column=9, data="不通过", sheet="withdraw")
            logger.info("测试用例{}:{}执行失败".format(test_info["case_id"], test_info["title"]))
            raise e
        else:
            middle_handler.Handler.excel.write(row=1 + test_info["case_id"], column=9, data="通过", sheet="withdraw")
            logger.info("测试用例{}:{}执行通过".format(test_info["case_id"], test_info["title"]))

    def tearDown(self) -> None:
        self.db.close()


if __name__ == '__main__':
    unittest.main()
