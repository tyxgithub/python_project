import ddt
from middleware import middle_handler
import unittest
from common import request_handler
import json
from decimal import Decimal

# 初始化logger
logger = middle_handler.Handler.logger
# 初始化excel数据
test_data = middle_handler.Handler.excel.read_data("recharge")


@ddt.ddt
class TestRecharge(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.token = middle_handler.Handler().token
        cls.member_id = middle_handler.Handler().member_id

    def setUp(self) -> None:
        self.db = middle_handler.Handler.db_class()

    @ddt.data(*test_data)
    def test_recharge(self, test_info):
        headers = middle_handler.Handler().replace_data(test_info["headers"])
        headers = eval(headers)
        data = middle_handler.Handler().replace_data(test_info["data"])
        data = eval(data)
        # if "#member_id#" in test_info["data"]:
        #     test_info["data"]=test_info["data"].replace("#member_id#",str(self.member_id))
        # if "#token#" in test_info["headers"]:
        #     test_info["headers"]=test_info["headers"].replace("#token#",self.token)
        before_money = self.db.query("select leave_amount from futureloan.member where id={}".format(self.member_id))[
            "leave_amount"]
        res = request_handler.visit(method=test_info["method"],
                                    url=middle_handler.Handler.yaml["host"] + test_info["url"],
                                    json=data,
                                    headers=headers)
        try:
            if res["code"] == 0:
                after_money = \
                    self.db.query("select leave_amount from futureloan.member where id={}".format(self.member_id))[
                        "leave_amount"]
                self.assertTrue(before_money + Decimal(str(json.loads(test_info["data"])["amount"])) == after_money)
            if res["code"] != 0:
                for key, value in json.loads(test_info["expected"]).items():
                    self.assertTrue(res[key] == value)
            logger.info("测试用例{}:{},执行通过".format(test_info["case_id"], test_info["title"]))
        except Exception as e:
            middle_handler.Handler.excel.write(row=1 + test_info["case_id"], column=9, data="不通过", sheet="recharge")
            logger.info("测试用例{}:{},执行失败".format(test_info["case_id"], test_info["title"]))
            raise e
        else:
            middle_handler.Handler.excel.write(row=1 + test_info["case_id"], column=9, data="通过", sheet="recharge")

    def tearDown(self) -> None:
        self.db.close()


if __name__ == '__main__':
    unittest.main()
