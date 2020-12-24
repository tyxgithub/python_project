import unittest
import ddt
import os
from api.common.request_handler import *
import json
import random
from common.mysql_handler import *
from middleware import middle_handler

# 读取配置文件excel名称
# yaml_data=read_yaml(os.path.join(config.CON_PATH,"config.yaml"))
# case_file=yaml_data["excel"]["file"]
# print(yaml_data["logger"])
# 初始化logger
# logger_config=yaml_data["logger"]
# logger=getLogger(
#     name=logger_config["name"],
#     file=os.path.join(config.LOGGER_PATH,logger_config["file"]),
#     logger_level=logger_config["logger_level"],
#     stream_level=logger_config["stream_level"],
#     file_level=logger_config["file_level"]
# )


logger = middle_handler.Handler.logger
test_data = middle_handler.Handler.excel.read_data("register")
print(test_data)
# #获取excel数据
# excel_file=os.path.join(config.EXCEL_PATH,"cases.xlsx")
# xlsx=ExcelHandler(excel_file)
# test_data=xlsx.read_data("register")
# logger.info("正在读取excel测试数据，测试数据")
print(test_data)


@ddt.ddt
class TestRegister(unittest.TestCase):
    @ddt.data(*test_data)
    def test_register(self, test_info):
        id = test_info["case_id"]
        if "#phone#" in test_info["data"]:
            phone = self.random_phone()
            test_info["data"] = test_info["data"].replace("#phone#", phone)
        data = json.loads(test_info["data"])
        res = visit(url=middle_handler.Handler.yaml["host"] + test_info["url"],
                    method=test_info["method"],
                    json=data,
                    headers=json.loads(test_info["headers"]))
        # self.assertEqual(json.loads(test_info["expected"])["msg"],res["msg"])
        # self.assertEqual(json.loads(test_info["expected"])["code"], res["code"])
        # print (test_info["data"])
        try:
            for key, value in json.loads(test_info["expected"]).items():
                self.assertTrue(value == res[key])
            if res["code"] == 0:
                db = middle_handler.Handler.db_class()
                user = db.query("select * from futureloan.member where mobile_phone={}".format(data["mobile_phone"]))
                self.assertTrue(user)
            middle_handler.Handler.logger.info("测试用例{}：{},执行成功".format(test_info["case_id"], test_info["title"]))
        except AssertionError as e:
            middle_handler.Handler.excel.write(row=id + 1, column=9, data="不通过", sheet="register")
            middle_handler.Handler.logger.info("测试用例{}：{},执行失败".format(test_info["case_id"], test_info["title"]))
            raise e
        else:
            middle_handler.Handler.excel.write(row=id + 1, column=9, data="通过", sheet="register")

    def random_phone(self):
        # 随机生成一个动态手机号码，用来成功注册
        # 需要查询数据
        while True:
            phone = "1" + random.choice(["3", "5"])
            for i in range(0, 9):
                num = random.randint(0, 9)
                phone += str(num)
            # db = MysqlHandler(host="120.78.128.25", port=3306, user="future", password="123456", charset="utf8",
            #                   cursorclass=DictCursor)
            # phone_record=db.query("select * from futureloan.member  where mobile_phone={}".format(phone))
            phone_record = middle_handler.Handler.db_class().query(
                "select * from futureloan.member  where mobile_phone={}".format(phone))
            if not phone_record:
                middle_handler.Handler.db_class().close()
                return phone
            middle_handler.Handler.db_class().close()


if __name__ == '__main__':
    # unittest.main()
    print(test_data)