# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import json
import time
import unittest

# from scripts.Base import Base
from math import floor

from scripts.backend.backend_base import BackendBase
from scripts.friend_and_chat.friend_base import FriendBase
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config
from scripts.logins.login_base import LoginBase
from scripts.user_info.user_base import UserBase
from scripts.handle_log import do_log


class IntroduceReceive(unittest.TestCase):
    """
    邀请有奖-任务列表，送礼
    """
    # 用户信息
    A = '{"mobile": "17700000000", "password": "123456"}'
    B = '{"mobile": "17700000002", "password": "123456"}'
    C = '{"mobile": "17700000007", "password": "123456"}'
    D = '{"mobile": "17621620738", "password": "123456"}'

    def test_case_01(self):
        # 1.登录,获取下级用户的id

        c_login_actual = LoginBase().login(self.C)
        # c_login_token = c_login_actual.json()["token"]
        c_user_id = c_login_actual.json()["user_info"]["id"]
        c_gender = c_login_actual.json()["user_info"]["gender"]
        c_vip = c_login_actual.json()["user_info"]["vip"]
        print(c_vip)

        # 查询用户a的邀请有奖可领取数量
        a_login_actual = LoginBase().login(self.A)
        a_login_token = a_login_actual.json()["token"]
        a_user_id = a_login_actual.json()["user_info"]["id"]

        # 2.获取下级邀请人的可领取信息

        # 获取用户邀请有奖的数量
        # introduce_receive_actual = UserBase().introduce_receive(a_login_token, c_user_id)
        # introduce_receive_list = introduce_receive_actual.json()["list"]
        Superior_before_receive_num = UserBase().introduce_receive_num(a_login_token, c_user_id)
        print(Superior_before_receive_num)

        login_actual = LoginBase().login(self.D)
        login_token = login_actual.json()["token"]
        Up_Superior_before_receive_num = UserBase().introduce_receive_num(login_token, a_user_id)
        print(Up_Superior_before_receive_num)
        # 3.下级邀请人，完成任务（收礼，充值）
        # 3.1 完成任务
        # 3.1.1 男生获得10000钻石已上充值一次,或者vip + 1
        # 3.1.2 女生获得10000钻石已上充值一次,或者vip + 1
        data_list = {"user_id": c_user_id, "vip": (int(c_vip)+1)}
        backend_token = LoginBase().get_backend_token(do_config("admin", "A"))

        actual = BackendBase().updata_userinfo(backend_token, data_list)
        print(actual.json())

        # 4.登录，上级邀请人查看可领取的任务信息
        # 获取下级邀请人的可领取信息,查询可领取数量
        a_login_actual = LoginBase().login(self.A)
        a_login_token = a_login_actual.json()["token"]

        # 5.获取下级邀请人的可领取信息
        time.sleep(20)
        # 获取用户邀请有奖的数量
        # introduce_receive_actual = UserBase().introduce_receive(a_login_token, c_user_id)
        # introduce_receive_list = introduce_receive_actual.json()["list"]
        Superior_after_receive_num = UserBase().introduce_receive_num(a_login_token, c_user_id)
        login_actual = LoginBase().login(self.D)
        login_token = login_actual.json()["token"]
        Up_Superior_after_receive_num = UserBase().introduce_receive_num(login_token, a_user_id)
        print(Superior_after_receive_num)
        print(Up_Superior_after_receive_num)
        # 6.断言，根据性别判断，（充值、收礼完成的任务数目）
        print("完成的任务数目为：{}".format(1))
        verdict = (-1, 0, 1)
        down_receive_num = Superior_before_receive_num[0] + 1 - Superior_after_receive_num[0]
        up_receive_num = Up_Superior_before_receive_num[0] + 1 - Up_Superior_after_receive_num[0]
        try:
            self.assertIn(down_receive_num, verdict)
            self.assertIn(up_receive_num, verdict)
            # self.assertEqual(Superior_before_receive_num[1], Superior_after_receive_num[1])
            # self.assertEqual(Up_Superior_before_receive_num[1], Up_Superior_after_receive_num[1])
        except AssertionError as e:
            do_log.error("具体异常为：{}".format(e))
            raise e
        else:
            print("ok")


if __name__ == '__main__':
    unittest.main()



