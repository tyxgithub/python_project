import pymysql
from pymysql.cursors import DictCursor

'''
域名
端口
用户名
密码
编码格式
返回数据格式为字典
'''


class MysqlHandler():
    def __init__(self,
                 host=None,
                 port=3306,
                 user=None,
                 password=None,
                 charset="utf8",
                 cursorclass=DictCursor
                 ):
        # 建立mysql数据库连接
        self.con = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset=charset,
            cursorclass=cursorclass  # 游标类，可以把元祖数据转为字典
        )
        self.cursor = self.con.cursor()

    def query(self, sql, oneResult=True):
        try:
            self.con.commit()
            print ("数据库事务提交成功")
            print(self.con.commit())
            self.cursor.execute(sql)
        except Exception as e:
            raise e
            return "sql执行错误，可能原因，数据库sql语句错误"

        else:
            if oneResult:
                return self.cursor.fetchone()
            return self.cursor.fetchall()
        self.close()

    def close(self):
        self.cursor.close()
        self.con.close()


if __name__ == '__main__':
    db = MysqlHandler(host="120.78.128.25", port=3306, user="future", password="123456", charset="utf8",
                      cursorclass=DictCursor)
    # print(db.query("select * from futureloan.member  where mobile_phone={}".format(15252993570)))
    # print(db.query("select * from futureloan.member  where mobile_phone={}".format(18538783344)))
    print(db.query("select * from futureloan.loan  where member_id={}".format(12305), oneResult=False))
    print(len(db.query("select * from futureloan.loan  where member_id={}".format(12305), oneResult=False)))
