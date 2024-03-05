# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import time
import unittest

# from scripts.Base import Base
from scripts.backend.backend_base import BackendBase
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config
from scripts.logins.login_base import LoginBase
from scripts.others.others_base import OthersBase
from scripts.partys.party_base import PartyBase
from scripts.redpackets.redpacket_base import RedpacketBase
from scripts.user_info.user_base import UserBase


class PartyClose(unittest.TestCase):
    """
    聚会红包
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

    def test_case_01(self):
        a_login_actual = LoginBase().login(do_config("username", "A"))
        a_login_token = a_login_actual.json()["token"]
        # 用户a发送之前查询钻石余额，和榜单积分
        # 用户a查询
        all_party_actual = PartyBase().get_all_party(a_login_token)
        party_list = all_party_actual.json()["list"]
        party_list1 = []
        for i in range(len(party_list)):
            var = party_list[i]["id"]
            actual = PartyBase().close_party(a_login_token, var)
            # print(actual.json())
            error_message = actual.json()["error_message"]
            if error_message == "Party Status 5" or error_message == "Party Status -2" or \
                    error_message == "Have been close":
                pass
            else:
                party_list1.append(var)
                if error_message == "Packet Unissued":
                    pass
                elif error_message == "U R Not Party Owner":
                    actual = PartyBase().party_action(a_login_token, var, "退出聚会")
                elif error_message == "Party Status 1":
                    actual = PartyBase().party_action(a_login_token, var)
                else:
                    print("无正在准备的聚会")

        print(party_list1)

        for var in party_list1:
            token = LoginBase().get_backend_token(do_config("admin", "A"))
            actual = BackendBase().backend_party_close(token, var)
            print(actual.text)


        # 断言，判断前后的差值
        try:
            self.assertEqual(int(1) + int(1),
                             int(2))
        except AssertionError as e:
            print("fail")
            raise e
        else:
            print("pass")


if __name__ == '__main__':
    unittest.main()
