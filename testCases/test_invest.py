import unittest
import json
from middleware import middle_handler
from common.request_handler import *
import ddt

# 初始化hander对象
env_data = middle_handler.Handler()
# 初始化logger
logger = env_data.logger
# 初始化数据
test_data = env_data.excel.read_data("invest")


@ddt.ddt
class TestInvest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.token = env_data.token
        cls.member_id = env_data.member_id

    def setUp(self) -> None:
        setattr(env_data, "loan_id", env_data.add_loan())
        env_data.audit_loan()
        env_data.recharge()
        self.db = env_data.db_class()

    def tearDown(self) -> None:
        self.db.close()

    @ddt.data(*test_data)
    def test_invest(self, test_info):
        data = env_data.replace_data(test_info["data"])
        data = eval(data)
        headers = test_info["headers"]
        headers = env_data.replace_data(headers)
        headers = json.loads(headers)

        try:
            # 查询之前的余额
            if test_info["check_sql"]:
                member = self.db.query("select * from futureloan.member where id={}".format(self.member_id))
                money_befoer = member["leave_amount"]

                before_loan = self.db.query("select * from futureloan.invest where "
                                            "member_id={}".format(self.member_id), oneResult=False)
            res = visit(url=env_data.yaml["host"] + test_info["url"],
                        method=test_info["method"],
                        json=data,
                        headers=headers)
            if res["code"] == 0:
                after_loan = self.db.query("select * from futureloan.member where id={}".format(
                    self.member_id), oneResult=False)
                self.assertEqual(len(before_loan) + 1, len(after_loan))
                member_after = self.db.query("selct * from futureloan.member where id={}".format(self.member_id))
                money_after = member_after['leave_amount']
                self.assertEqual(money_befoer - data["amount"], money_after)
        except Exception as e:
            env_data.excel.write(row=1 + test_info["case_id"], column=9, data="不通过", sheet="recharge")
            logger.info("测试用例{}：{},执行失败".format(test_info["case_id"], test_info["title"]))
            raise e
        else:
            env_data.excel.write(row=1 + test_info["case_id"], column=9, data="通过", sheet="recharge")
            logger.info("测试用例{}：{},执行成功".format(test_info["case_id"], test_info["title"]))


if __name__ == '__main__':
    unittest.main()
