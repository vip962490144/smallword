#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random

import pymysql

from scripts.handle_config import do_config


class HandleMysql:
    """
    数据库处理类
    """

    def __init__(self):
        # 创建连接
        self.connect_one = pymysql.connect(host=do_config("mysql", "host"),
                                           user=do_config("mysql", "user"),
                                           password=str(do_config("mysql", "password")),
                                           db=do_config("mysql", "db"),
                                           port=do_config("mysql", "port"),
                                           charset=do_config("mysql", "charset"),
                                           cursorclass=pymysql.cursors.DictCursor)
        # 创建游标
        self.cursor = self.connect_one.cursor()

    def __call__(self, sql, arg=None, is_more=False):
        """
        获取值
        :param sql:sql查询语句。
        :param arg:参数，只能是序列类型。可以带入%s（占位符）处。
        :param is_more: 判读获取多个值还是一个值，默认False获取一个值
        :return:
        """
        self.cursor.execute(sql, arg)
        self.connect_one.commit()

        if is_more:
            result = self.cursor.fetchall()
        else:
            result = self.cursor.fetchone()

        return result

    @staticmethod
    def create_moblie():
        """
        随机生成11位手机号。
        :return:
        """
        start_mobile = ('139', '138', '137', '136', '135', '134', '159', '158', '157', '152', '151', '150', '188',
                        '187', '130', '131', '132', '155', '156', '186', '185', '133', '153', '189', '180')
        start_num = random.choice(start_mobile)
        one_str = "0123456789"
        end_num = "".join(random.sample(one_str, 8))
        return start_num + end_num

    @staticmethod
    def create_user_id():
        one_str = "0123456789"
        num = "".join(random.sample(one_str, 6))
        return num

    @staticmethod
    def create_loan_id():
        one_str = "0123456789"
        num = "".join(random.sample(one_str, 6))
        return num

    def is_existed_mobile(self, mobile):
        """
        判断给定的手机号在数据库中是否存在
        :param mobile:待判断的手机号，为字符串类型
        :return: True or False
        """
        sql = "SELECT `MobilePhone` FROM future.`member` WHERE `MobilePhone`=%s"
        if self(sql, arg=(mobile, )):
            return True
        else:
            return False

    def is_existed_load_id(self, load_id):
        """
        判断给定的id号在数据库中是否存在
        :param load_id:待判断的id号，为字符串类型
        :return: True or False
        """
        sql = "SELECT `Id` FROM future.`loan` WHERE `Id`=%s"
        if self(sql, arg=(load_id, )):
            return True
        else:
            return False

    def is_existed_user_id(self, user_id):
        """
        判断给定的user_id号在数据库中是否存在
        :param user_id:待判断的id号，为字符串类型
        :return: True or False
        """
        sql = "SELECT `MemberID` FROM future.`loan` WHERE `MemberID`=%s"
        if self(sql, arg=(user_id, )):
            return True
        else:
            return False

    def is_existed_mobile_amount(self, mobile):
        """
        判断手机号存在，则返回该用户的id
        :param mobile:
        :return:
        """
        sql = "SELECT `LeaveAmount` FROM future.`member` WHERE `MobilePhone`=%s"
        return self(sql, arg=(mobile, ))['LeaveAmount']

    def create_not_mobile(self):
        """
        判断手机号是否存在，无限循环，直到取出一个不存在的手机号。
        :return:
        """
        while True:
            one_mobile = self.create_moblie()
            if not self.is_existed_mobile(one_mobile):
                break

        return one_mobile

    def create_not_load_id(self):
        while True:
            load_id = self.create_loan_id()
            if not self.is_existed_load_id(load_id):
                break

        return load_id

    def create_not_user_id(self):
        while True:
            user_id = self.create_user_id()
            if not self.is_existed_user_id(user_id):
                break

        return user_id

    def close(self):
        """
        关闭游标，关闭连接
        :return:
        """
        self.cursor.close()
        self.connect_one.close()


if __name__ == '__main__':
    sql_1 = "SELECT * FROM invest LIMIT 0, 10;"
    sql_2 = "SELECT * FROM member WHERE leaveAmount > %s LIMIT 0, 10;"

    do_mysql = HandleMysql()
    result1 = do_mysql(sql=sql_1, is_more=True)
    print(result1)
    # print(do_mysql(sql=sql_2, arg=(600,)))
    # print(do_mysql.create_not_mobile())
    do_mysql.close()
