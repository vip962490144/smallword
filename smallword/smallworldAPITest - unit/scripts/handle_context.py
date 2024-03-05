#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from scripts.handle_pymusql import HandleMysql
from scripts.handle_config import HandleConfig
from scripts.constants import CONFIG_USER_FILE_PATH

do_config = HandleConfig(CONFIG_USER_FILE_PATH)


class HandleContext:
    """
    实现参数化，
    """
    not_exited_pattern = re.compile(r"\$\{not_exited_tel}")
    invest_user_pattern = re.compile(r"\$\{invest_user_tel}")
    invest_user_pwd_pattern = re.compile(r"\$\{invest_user_pwd}")
    invest_user_id_pattern = re.compile(r"\$\{invest_user_id}")
    borrow_user_pattern = re.compile(r"\$\{borrow_user_id}")
    admin_user_pattern = re.compile(r"\$\{admin_user_tel}")
    admin_user_pwd_pattern = re.compile(r"\$\{admin_user_pwd}")
    load_id_pattern = re.compile(r"\$\{loan_id}")
    not_exited_user_id_pattern = re.compile(r"\$\{not_exited_user_id}")
    not_exited_loan_id_pattern = re.compile(r"\$\{not_exited_loan_id}")
    record_id_pattern = re.compile(r"\$\{record_id}")
    user_amount_pattern = re.compile(r"\$\{user_amount}")

    @classmethod
    def not_exited_replace(cls, data):
        """
        把data参数中的匹配模式数据替换。使用未注册的手机号替换。
        :param data:
        :return:
        """
        do_mysql = HandleMysql()
        if re.search(cls.not_exited_pattern, data):
            data = re.sub(cls.not_exited_pattern, do_mysql.create_not_mobile(), data)
        if re.search(cls.not_exited_user_id_pattern, data):
            data = re.sub(cls.not_exited_user_id_pattern, do_mysql.create_not_user_id(), data)
        if re.search(cls.not_exited_loan_id_pattern, data):
            data = re.sub(cls.not_exited_loan_id_pattern, do_mysql.create_not_load_id(), data)
        do_mysql.close()
        return data

    @classmethod
    def invest_user_replace(cls, data):
        if re.search(cls.invest_user_pattern, data):
            data = re.sub(cls.invest_user_pattern, str(do_config("invest_user", "mobilephone")), data)
        if re.search(cls.invest_user_pwd_pattern, data):
            data = re.sub(cls.invest_user_pwd_pattern, str(do_config("invest_user", "pwd")), data)
        if re.search(cls.invest_user_id_pattern, data):
            data = re.sub(cls.invest_user_id_pattern, str(do_config("invest_user", "id")), data)
        return data

    @classmethod
    def borrow_user_replace(cls, data):
        if re.search(cls.borrow_user_pattern, data):
            data = re.sub(cls.borrow_user_pattern, str(do_config("borrow_user", "id")), data)

        return data

    @classmethod
    def admin_user_replace(cls, data):
        if re.search(cls.admin_user_pattern, data):
            data = re.sub(cls.admin_user_pattern, str(do_config("admin_user", "mobilephone")), data)
        if re.search(cls.admin_user_pwd_pattern, data):
            data = re.sub(cls.admin_user_pwd_pattern, str(do_config("admin_user", "pwd")), data)

        return data

    @classmethod
    def load_id_replace(cls, data):
        """
        替换，放入load_id
        :param data:
        :return:
        """
        if re.search(cls.load_id_pattern, data):
            load_id = str(getattr(cls, "load_id"))
            data = re.sub(cls.load_id_pattern, load_id, data)

        return data

    @classmethod
    def record_id_replace(cls, data):
        """
        替换，放入load_id
        :param data:
        :return:
        """
        if re.search(cls.record_id_pattern, data):
            record_id = str(getattr(cls, "record_id"))
            data = re.sub(cls.record_id_pattern, record_id, data)

        return data

    @classmethod
    def user_amount_replace(cls, data):
        """
        替换，放入load_id
        :param data:
        :return:
        """
        if re.search(cls.user_amount_pattern, data):
            user_amount = str(getattr(cls, "user_amount"))
            data = re.sub(cls.user_amount_pattern, user_amount, data)

        return data

    @classmethod
    def register_parameterization(cls, data):
        """
        实现注册功能的参数化
        :param data:
        :return:
        """
        # 先替换未注册的手机号,load_id号，user_id号。
        data = cls.not_exited_replace(data)
        # 先替换未注册的手机号
        data = cls.not_exited_replace(data)
        # 先替换未注册的手机号
        data = cls.not_exited_replace(data)
        # 再替换投标的人员的手机号，也可以当做已注册的人员信息。
        data = cls.invest_user_replace(data)
        # 再替换管理员的手机号
        data = cls.admin_user_replace(data)
        # 在替换加标的人员信息
        data = cls.borrow_user_replace(data)
        # 在替换标的id信息。
        data = cls.load_id_replace(data)
        return data


if __name__ == '__main__':
    pass





