# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import time
import unittest

from scripts.activities_and_discoveries.discover_base import DiscoverBase
from scripts.clubs.club_base import ClubBase
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config
from scripts.logins.login_base import LoginBase
from scripts.others.others_base import OthersBase
from scripts.redpackets.redpacket_base import RedpacketBase
from scripts.user_info.user_base import UserBase


class ClubSecretaryPacket(unittest.TestCase):
    """
    俱乐部秘书红包：逻辑还未修改
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

        # 修改获取当前时间id，修改俱乐部时间
        time_id = ClubBase().get_time_id(a_login_token)
        data_list = {"name": "红红火火恍恍惚惚", "gender_limit": 3,
             "send_time_id": time_id, "packet_money": 30,
                     "notice": "红红火火恍恍惚惚", "flag_chat": 1}
        ClubBase().club_info_update(a_login_token, 5109, data_list)
        actual = ClubBase().get_clubs_info(a_login_token, 5109)

        member_num = actual.json()["member_num"]

        time.sleep(5)
        actual = RedpacketBase().everyday_redpacket()

        # 用户b领取之前查询礼券余额，和榜单积分
        # 执行用户B登录操作
        b_login_actual = LoginBase().login(do_config("username", "B"))
        b_login_token = b_login_actual.json()["token"]
        b_user_id = b_login_actual.json()["user_info"]["id"]
        # 查询用户b的榜单积分和礼券
        b_user_info_befoer = UserBase().get_user_info(b_login_token, "nickname,ticket")
        b_user_info_befoer_ticket = b_user_info_befoer.json()["ticket"]
        b_user_info_befoer_rank = OthersBase().get_user_ranking(b_login_token, b_user_id, "魅力榜")

        # 查询奖池钻石
        guess_diamond_actual = DiscoverBase().get_guess_diamond(b_login_token)
        guess_befoer_diamond = guess_diamond_actual.json()["diamond"]

        # 发送之后等待一段时间，等红包发送成功。
        time.sleep(5)
        actual = ClubBase().get_packet_detail(b_login_token, 5109)
        print(actual.status_code)
        code = actual.status_code
        if int(code) == 200:
            redpacket_id = actual.json()["packet_id"]
        else:
            print("无可领取的每日红包")
            exit()

        # 用户b领取红包
        receive_redpacket = RedpacketBase().receive_redpacket(b_login_token, redpacket_id)
        # 获得领取红包的金额
        receive_redpacket_money = receive_redpacket.json()["packet"]["current_user_packet_money"]

        receive_redpacket_ticket = float(receive_redpacket_money) * 13
        if receive_redpacket_ticket > 100:
            guess_diamond = receive_redpacket_ticket * 0.1
            receive_redpacket_ticket *= 0.95
            guess_diamond = round(guess_diamond, 0)
        else:
            guess_diamond = 0

        receive_redpacket_ticket = round(receive_redpacket_ticket, 0)

        # print(receive_redpacket_ticket, type(receive_redpacket_ticket))

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

        # 查询奖池钻石
        guess_diamond_actual = DiscoverBase().get_guess_diamond(a_login_token)
        guess_after_diamond = guess_diamond_actual.json()["diamond"]

        verdict = (-1, 0, 1)
        ticket_num = int(b_user_info_befoer_ticket) + int(receive_redpacket_ticket) - \
                     int(b_user_info_after_ticket)
        guess_diamond_num = int(guess_befoer_diamond) + int(guess_diamond) - int(guess_after_diamond)
        user_packet_num = int(member_num) - 1
        consumption_diamond = int(data_list["packet_money"]) * 13 * user_packet_num
        b_user_rank_num = int(b_user_info_befoer_rank) + round(float(receive_redpacket_money) * 13, 0)
        a_user_rank_num = int(a_user_info_befoer_rank) + round(float(receive_redpacket_money) * 13, 0)

        # 断言，判断前后的差值
        try:
            self.assertEqual(int(a_user_info_after_diamond) + consumption_diamond,
                             int(a_user_info_befoer_diamond))
            self.assertIn(a_user_rank_num - int(a_user_info_after_rank), verdict)
            self.assertIn(b_user_rank_num - int(b_user_info_after_rank), verdict)
            self.assertIn(ticket_num, verdict)
            self.assertIn(guess_diamond_num, verdict)
        except AssertionError as e:
            print("fail")
            raise e
        else:
            print("发送红包用户的钻石余额为{}，领取红包用户的礼券余额为{}，奖池金额为{}"
                  .format(a_user_info_after_diamond, b_user_info_after_ticket, guess_after_diamond))
            print("发送红包用户的实力榜积分为{}，领取红包用户的魅力榜积分为{}"
                  .format(a_user_info_after_rank, b_user_info_after_rank))
            print("领取的礼券为{}，进入奖池的金额为{}".format(receive_redpacket_ticket, guess_diamond))
            print("pass")


if __name__ == '__main__':
    unittest.main()
