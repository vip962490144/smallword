# -*- coding:utf-8 -*-
# @Author:Jaden.wang
import time
import unittest

from scripts.Base import Base
from scripts.friend_and_chat.friend_base import FriendBase
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config
from scripts.logins.login_base import LoginBase
from scripts.others.others_base import OthersBase
from scripts.user_info.user_base import UserBase


class GiftRecord(unittest.TestCase):
    """
    赠送礼物,收取礼物，断言
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
        # 查询请求前：用户a钻石，查询用户b的榜单积分和礼券数目
        a_login_actual = LoginBase().login(do_config("username", "A"))
        a_login_token = a_login_actual.json()["token"]
        a_user_id = a_login_actual.json()["user_info"]["id"]
        a_user_info_befoer = UserBase().get_user_info(a_login_token, "nickname,diamond")
        a_user_info_befoer_diamond = a_user_info_befoer.json()["diamond"]
        a_user_info_befoer_rank = OthersBase().get_user_ranking(a_login_token, a_user_id, "实力榜")

        # 获取礼物id，并且查询赠送的礼物的价值
        gift_id = FriendBase().get_gift_id(a_login_token)
        print(gift_id)
        gift_value = FriendBase().get_gift_value(a_login_token, gift_id)
        # 执行用户A赠送操作，查询赠送礼物的记录id,查询礼物的价值,private_flag=0私密送礼
        send_data = {"gift_id": gift_id, "receiver_id": 12707, "apply_content": "mmmm",
                     "flag_apply": 0, "num": 1, "private_flag": 1}
        record_id = FriendBase().get_record_id(a_login_token, send_data)

        # 执行用户B登录操作
        b_login_actual = LoginBase().login(do_config("username", "B"))
        b_login_token = b_login_actual.json()["token"]
        b_user_id = b_login_actual.json()["user_info"]["id"]
        # 查询用户b的榜单积分和礼券
        b_user_info_befoer = UserBase().get_user_info(b_login_token, "nickname,ticket")
        b_user_info_befoer_ticket = b_user_info_befoer.json()["ticket"]
        b_user_info_befoer_rank = OthersBase().get_user_ranking(b_login_token, b_user_id, "魅力榜")

        print(a_user_info_befoer.json(), a_user_info_befoer_rank, b_user_info_befoer.json(), b_user_info_befoer_rank)

        # 请求
        # 用户B执行接收礼物操作，使用记录id，进行接收操作
        actual = FriendBase().receive_gift(b_login_token, record_id)
        # print(actual.json())

        # 等待一会，等待计算到服务器生效
        time.sleep(3)

        # 查询用户a的钻石余额变动， 查询赠送的礼物价值
        # 执行用户A登录操作
        a_login_actual = LoginBase().login(do_config("username", "A"))
        a_login_token = a_login_actual.json()["token"]
        a_user_id = a_login_actual.json()["user_info"]["id"]
        a_user_info_after = UserBase().get_user_info(a_login_token, "nickname,diamond")
        a_user_info_after_diamond = a_user_info_after.json()["diamond"]
        a_user_info_after_rank = OthersBase().get_user_ranking(a_login_token, a_user_id, "实力榜")


        # 执行用户B登录操作
        b_login_actual = LoginBase().login(do_config("username", "B"))
        b_login_token = b_login_actual.json()["token"]

        # 查询用户b的榜单积分和礼券
        b_user_info_after = UserBase().get_user_info(b_login_token, "nickname,ticket")
        b_user_info_after_ticket = b_user_info_after.json()["ticket"]
        b_user_info_after_rank = OthersBase().get_user_ranking(b_login_token, b_user_id, "魅力榜")

        print(a_user_info_after.json(), a_user_info_after_rank, b_user_info_after.json(), b_user_info_after_rank)

        # 查询请求后：用户a钻石，查询用户b的榜单积分和礼券数目，对比
        try:
            if send_data["private_flag"] == 0:

                self.assertEqual(int(a_user_info_after_rank), int(a_user_info_befoer_rank))
            else:
                self.assertEqual(int(a_user_info_after_rank),
                                 (int(a_user_info_befoer_rank) + int(gift_value)))
            self.assertEqual(int(a_user_info_befoer_diamond),
                                 (int(a_user_info_after_diamond) + int(gift_value)))
            self.assertEqual(int(b_user_info_after_ticket),
                             (int(b_user_info_befoer_ticket) + int(gift_value)))
            self.assertEqual(int(b_user_info_after_rank),
                             (int(b_user_info_befoer_rank) + int(gift_value)))
        except AssertionError as e:
            print("测试赠送礼物失败")
            raise e
        else:
            print("测试赠送礼物成功")


if __name__ == '__main__':
    unittest.main()
