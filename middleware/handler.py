from config import config
from api.common import yaml_handler, excel_handler, log_handler, mysql_handler, request_handler
import os
from pymysql.cursors import DictCursor
import jsonpath


class MysqlHandlerMid(mysql_handler.MysqlHandler):
    '''读取配置文件的选项，MysqlHandler'''

    def __init__(self):
        '初始化所有配置项'
        db_config = Handler.yaml["db"]
        super().__init__(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["user"],
            password=db_config["password"],
            charset=db_config["charset"],
            cursorclass=DictCursor

        )


class Handler():
    # 中间层，初始化所有数据

    loan_id = None
    # 加载python配置项
    conf = config

    # 加载YAML配置项
    yaml = yaml_handler.read_yaml(os.path.join(config.CON_PATH, "config.yaml"))

    # excel数据
    __excel_path = conf.EXCEL_PATH
    __excel_file = yaml["excel"]['file']
    excel = excel_handler.ExcelHandler(os.path.join(__excel_path, __excel_file))

    # logger
    __logger_config = yaml["logger"]
    logger = log_handler.getLogger(
        name=__logger_config["name"],
        file=os.path.join(config.LOGGER_PATH, __logger_config["file"]),
        logger_level=__logger_config["logger_level"],
        stream_level=__logger_config["stream_level"],
        file_level=__logger_config["file_level"]
    )

    def login(self, user):
        res = request_handler.visit(method="post",
                                    url=Handler.yaml["host"] + "/member/login",
                                    json=user,
                                    headers={"Accept": "*/*",
                                             "Content-Type": "application/json",
                                             "X-Lemonban-Media-Type": "lemonban.v2"}
                                    )
        # jsonpath返回的是一个List数据
        token_type = jsonpath.jsonpath(res, "$..token_type")[0]
        token_str = jsonpath.jsonpath(res, "$..token")[0]
        token = " ".join([token_type, token_str])

        member_id = jsonpath.jsonpath(res, "$..id")[0]
        return {"token": token, "member_id": member_id}

    # 不存储对象。存储类
    db_class = MysqlHandlerMid

    @property
    def token(self):
        return self.login(self.yaml["login"])["token"]

    @property
    def member_id(self):
        return self.login(self.yaml["login"])["member_id"]

    @property
    def admin_token(self):
        return self.login(self.yaml["admin_user"])["token"]

    # @property
    # def loan_id(self):
    #     return self.add_loan()
    def add_loan(self):
        data = {
            "member_id": self.member_id,
            "title": "tyx项目新增",
            "amount": 2000.00,
            "loan_rate": 18.0,
            "loan_term": 6,
            "loan_date_type": 1,
            "bidding_days": 10
        }
        res = request_handler.visit(
            method="post",
            url=Handler.yaml["host"] + "/loan/add",
            headers={"X-Lemonban-Media-Type": "lemonban.v2", "Authorization": self.token},
            json=data
        )
        # jsonpath返回匹配list
        return jsonpath.jsonpath(res, "$..id")[0]

    # 属性替换，自动完成Handler中property方法的属性替换
    def replace_data(self, data):
        import re
        pattern = r"#(.*?)#"
        while re.search(pattern, data):
            key = re.search(pattern, data).group(1)
            value = getattr(self, key, "")
            data = re.sub(pattern, str(value), data, count=1)
        return data

    def audit_loan(self):
        '''审核项目'''
        data = {"loan_id": self.loan_id, "approved_or_not": True}
        res = request_handler.visit(
            method="patch",
            url=self.yaml["host"] + "/loan/audit",
            headers={"X-Lemonban-Media-Type": "lemonban.v2", "Authorization": self.token},
            json=data
        )

    def recharge(self):
        '''充值'''
        data = {"member_id": self.member_id, "amount": 5000}
        res = request_handler.visit(
            method="post",
            url=self.yaml["host"] + "/loan/recharge",
            headers={"X-Lemonban-Media-Type": "lemonban.v2", "Authorization": self.token},
            json=data
        )


if __name__ == '__main__':
    data_path = Handler.conf.EXCEL_PATH
    # print (data_path)
    # print(Handler.yaml)
    # print(Handler.excel.read_data("login"))
    # print(Handler.logger)
    # db=MysqlHandlerMid()
    # print (Handler.db_class().query("select leave_amount from futureloan.member where id={}".format(login()["member_id"])))
    # print(login())
    # print(Handler().loan_id)
    # print(Handler().yaml)
    # print(Handler().replace_data('{"member_id":"#member_id#","token":"#token#"}'))
    # env_data=Handler()
    # setattr(env_data, "loan_id", env_data.add_loan())
    # print(env_data.loan_id)

