# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import time
import unittest

# from scripts.Base import Base
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config
from scripts.logins.login_base import LoginBase
from scripts.others.others_base import OthersBase
from scripts.redpackets.redpacket_base import RedpacketBase
from scripts.user_info.user_base import UserBase


class PartyWelfarePacket(unittest.TestCase):
    """
    聚会福利红包
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
        a_user_id = a_login_actual.json()["user_info"]["id"]
        a_user_info_befoer = UserBase().get_user_info(a_login_token, "nickname,diamond")
        a_user_info_befoer_diamond = a_user_info_befoer.json()["diamond"]
        a_user_info_befoer_rank = OthersBase().get_user_ranking(a_login_token, a_user_id, "实力榜")
        # 发送红包，获取红包id
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + a_login_token}
        data_list = {"party_id":"7507","type":"8","total_money": "100","memo":"美女才可以领",}
        redpacket_id = RedpacketBase().get_redpacket_id(a_login_token, data_list)
        # 用户b领取之前查询礼券余额，和榜单积分
        # 执行用户B登录操作
        b_login_actual = LoginBase().login(do_config("username", "B"))
        b_login_token = b_login_actual.json()["token"]
        b_user_id = b_login_actual.json()["user_info"]["id"]
        # 查询用户b的榜单积分和礼券
        b_user_info_befoer = UserBase().get_user_info(b_login_token, "nickname,ticket")
        b_user_info_befoer_ticket = b_user_info_befoer.json()["ticket"]
        b_user_info_befoer_rank = OthersBase().get_user_ranking(b_login_token, b_user_id, "魅力榜")

        # 领取之后等待几秒，等红包发送成功。
        time.sleep(3)

        # 用户b领取红包
        receive_redpacket = RedpacketBase().receive_redpacket(b_login_token, redpacket_id)
        # 获得领取红包的金额
        receive_redpacket_money = receive_redpacket.json()["packet"]["current_user_packet_money"]
        receive_redpacket_ticket = round(float(receive_redpacket_money) * 13, 0)

        # 领取之后等待几秒，等积分，钻石扣除生效。
        time.sleep(3)

        # 查询用户b的榜单积分和礼券
        b_user_info_after = UserBase().get_user_info(b_login_token, "nickname,ticket")
        b_user_info_after_ticket = b_user_info_after.json()["ticket"]
        b_user_info_after_rank = OthersBase().get_user_ranking(b_login_token, b_user_id, "魅力榜")

        # 用户a、b查询发送后的余额，查询领取后的榜单和礼券
        a_login_actual = LoginBase().login(do_config("username", "A"))
        a_login_token = a_login_actual.json()["token"]
        # 用户a发送之前查询钻石余额，和榜单积分
        # 用户a查询
        a_user_id = a_login_actual.json()["user_info"]["id"]
        a_user_info_after = UserBase().get_user_info(a_login_token, "nickname,diamond")
        a_user_info_after_diamond = a_user_info_after.json()["diamond"]
        a_user_info_after_rank = OthersBase().get_user_ranking(a_login_token, a_user_id, "实力榜")

        verdict = (-1, 0, 1)
        ticket_num = int(b_user_info_befoer_ticket) + int(receive_redpacket_ticket) - \
                     int(b_user_info_after_ticket)
        # 断言，判断前后的差值
        try:
            self.assertEqual(int(a_user_info_after_diamond) + int(data_list["total_money"]) * 13,
                             int(a_user_info_befoer_diamond))
            self.assertEqual(int(a_user_info_befoer_rank) + int(receive_redpacket_ticket),
                             int(a_user_info_after_rank))
            self.assertEqual(int(b_user_info_befoer_rank) + int(receive_redpacket_ticket),
                             int(b_user_info_after_rank))
            self.assertIn(ticket_num, verdict)
        except AssertionError as e:
            print("fail")
            raise e
        else:
            print("发送红包用户的钻石余额为{}，领取红包用户的礼券余额为{}"
                  .format(a_user_info_after_diamond, b_user_info_after_ticket))
            print("发送红包用户的实力榜积分为{}，领取红包用户的魅力榜积分为{}"
                  .format(a_user_info_after_rank, b_user_info_after_rank))
            print("领取的礼券为{}".format(receive_redpacket_ticket))
            print("pass")


if __name__ == '__main__':
    unittest.main()
