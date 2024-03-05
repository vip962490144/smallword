# -*- coding:utf-8 -*-
# @Author   :Jaden.wang

import unittest

from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config
from scripts.logins.login_base import LoginBase
from scripts.user_info.user_base import UserBase


class UserInfo(unittest.TestCase):
    """
    用户信息
    """
    @classmethod
    def setUpClass(cls):
        """
        所有测试类执行之前执行此程序。
        :return:
        """
        cls.send_res = HandleRequest()

    @classmethod
    def tearDownClass(cls):
        """
        所有测试类执行之后执行此程序。
        :return:
        """
        cls.send_res.close()

    # 获取用户数据
    def test_user_info(self):
        # |params|Yes|需要获取的字段。用逗号隔开。'nickname' 昵称；'vip' vip等级；'avatar'-头像地址；
        # 以下字段只有获取自己信息时会返回：'diamond'-钻石余额；'ticket'-礼券余额|
        # 获取用户信息
        user_login = LoginBase().login(do_config("username", "A"))
        user_loken = user_login.json()["token"]
        user_info_actual = UserBase().get_user_info(user_loken, "nickname,vip,ticket,diamond")
        user_info = user_info_actual.json()

        print(user_info)


if __name__ == '__main__':
    unittest.main()
