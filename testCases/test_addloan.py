import unittest
import json
from middleware import middle_handler
from common.request_handler import *
import ddt

# 初始化logger
logger = middle_handler.Handler.logger
# 初始化数据
test_data = middle_handler.Handler().excel.read_data("addloan")


@ddt.ddt
class TestAddLoan(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.token = middle_handler.Handler().token
        cls.member_id = middle_handler.Handler().member_id
        cls.db = middle_handler.Handler().db_class()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.close()

    @ddt.data(*test_data)
    def test_add_loan(self, test_info):
        headers = middle_handler.Handler().replace_data(test_info["headers"])
        headers = eval(headers)
        data = middle_handler.Handler().replace_data(test_info["data"])
        data = eval(data)

        before_count = len(
            self.db.query("select * from futureloan.loan  where member_id={}".format(str(self.member_id)),
                          oneResult=False))

        r = visit(method=test_info["method"],
                  url=middle_handler.Handler.yaml["host"] + test_info["url"],
                  json=data,
                  headers=headers)

        try:
            if r["code"] == 0:
                after_count = len(
                    self.db.query("select * from futureloan.loan  where member_id={}".format(str(self.member_id)),
                                  oneResult=False))
                self.assertTrue(before_count + 1 == after_count)
            else:
                for key, value in json.loads(test_info["expected"]).items():
                    self.assertTrue(r[key] == value)
        except Exception as e:
            logger.info("测试用例{}：{},执行失败".format(test_info["case_id"], test_info["title"]))
            middle_handler.Handler.excel.write(row=1 + test_info["case_id"], column=9, data="不通过", sheet="addloan")
            raise e
        else:
            logger.info("测试用例{}：{},执行成功".format(test_info["case_id"], test_info["title"]))
            middle_handler.Handler.excel.write(row=1 + test_info["case_id"], column=9, data="通过", sheet="addloan")


if __name__ == '__main__':
    unittest.main()
