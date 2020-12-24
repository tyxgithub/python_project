import unittest
from decimal import Decimal

import ddt
import json
from common import request_handler
from middleware.middle_handler import Handler

# 初始化数据
test_data = Handler.excel.read_data("audit")
logger = Handler.logger


@ddt.ddt
class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 拿到admin_token
        # 拿到普通token
        cls.token = Handler().token
        cls.member_id = Handler().member_id
        cls.admin_token = Handler().admin_token

    def setUp(self) -> None:
        # 添加项目
        self.db = Handler.db_class()
        self.loan_id = Handler().add_loan()

    def tearDown(self) -> None:
        self.db.close()

    @ddt.data(*test_data)
    def test_audit(self, test_info):
        data = test_info["data"]
        if "#loan_id#" in data:
            data = data.replace("#loan_id#", str(self.loan_id))

        if "#pass_loan_id#" in data:
            pass_loan = self.db.query("select * from futureloan.loan where status != 1 limit 10")
            data = data.replace("#pass_loan_id#", str(pass_loan["id"]))

        data = eval(data)

        headers = Handler().replace_data(test_info["headers"])
        headers = eval(headers)

        res = request_handler.visit(
            method=test_info["method"],
            url=Handler.yaml["host"] + test_info["url"],
            headers=headers,
            json=data
        )
        try:
            expected = json.loads(test_info["expected"])
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])

            if res["code"] == 0:
                # 验证状态
                loan = self.db.query("select status from futureloan.loan where id={}".format(self.loan_id))
                self.assertEqual(expected["status"], loan["status"])
        except Exception as e:
            logger.info("测试用例：{}，用例名称：{},执行失败".format(test_info["case_id"], test_info["title"]))
            Handler.excel.write(row=1 + test_info["case_id"], column=9, data="不通过", sheet="audit")
            raise e
        else:
            logger.info("测试用例：{}，用例名称：{},执行成功".format(test_info["case_id"], test_info["title"]))
            Handler.excel.write(row=1 + test_info["case_id"], column=9, data="通过", sheet="audit")


if __name__ == '__main__':
    unittest.TestCase()
