# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import datetime
import random
import time

from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase


class ClubBase:
    # 俱乐部操作类

    login_list = {}

    datalist = {}

    # 获取用户俱乐部列表
    def get_clubs(self, login_token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        clubs_list_url = do_config("api", "url") + "users/clubs"
        send_res = HandleRequest()
        actual = send_res(method="get", url=clubs_list_url, headers=headers)
        send_res.close()

        return actual

    # 获取俱乐部列表的列表
    def get_clubs_list(self, login_token):
        clubs_actual = self.get_clubs(login_token)
        # 我创建的俱乐部
        my_create_clubs_list = clubs_actual.json()["found_list"]
        # 我加入的俱乐部
        my_join_clubs_list = clubs_actual.json()["list"]

        return my_create_clubs_list, my_join_clubs_list

    # 获取俱乐部的人员信息
    def club_member(self, login_token, clubs_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        # club_member_list_url = "/clubs/{club_id}/users?pos={pos}&limit={limit}&type={type}"
        club_member_list_url = do_config("api", "url") + "clubs/{}/users?pos=0&limit=20".format(clubs_id)

        send_res = HandleRequest()
        actual = send_res(method="get", url=club_member_list_url, headers=headers)
        send_res.close()

        return actual

    # 获取俱乐部人员列表
    def get_club_menber_list(self, login_token, clubs_id):
        club_menber_list_actual = self.club_member(login_token, clubs_id)
        club_menber_list = club_menber_list_actual.json()["list"]

        return club_menber_list

    # 获取俱乐部详情
    @staticmethod
    def get_clubs_info(login_token, club_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        clubs_url = do_config("api", "url") + "/clubs/info?club_id={}".format(club_id)
        send_res = HandleRequest()
        actual = send_res(method="get", url=clubs_url, headers=headers)
        send_res.close()

        return actual

    # 修改俱乐部信息
    @staticmethod
    def club_info_update(login_token, club_id, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        clubs_url = do_config("api", "url") + "clubs/{}".format(club_id)
        send_res = HandleRequest()
        actual = send_res(method="PUT", url=clubs_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 获取俱乐部红包时间列表
    def club_packet_time_list(self, login_token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        clubs_url = do_config("api", "url") + "/clubs/send_time"
        send_res = HandleRequest()
        actual = send_res(method="GET", url=clubs_url, headers=headers)
        send_res.close()

        return actual

    # 获取当前时间的小时id
    def get_time_id(self, login_token):
        actual = self.club_packet_time_list(login_token)
        time_list = actual.json()["list"]
        a = int(time.time())    #当前时间
        c = datetime.datetime.fromtimestamp(a).strftime('%H')    #格式转换
        time_id = 1
        for var in range(len(time_list)):
            time_num = time_list[var]["time"]
            time_num = time_num[0:2]
            if int(time_num) == int(c):
                time_id = time_list[var]["id"]

        return time_id

    # 获取俱乐部是否能领每日红包
    def get_packet_detail(self, login_token, club_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        url = do_config("api", "url") + "clubs/{}/packet_accessibility".format(club_id)
        send_res = HandleRequest()
        actual = send_res(method="GET", url=url, headers=headers)
        send_res.close()

        return actual


if __name__ == '__main__':
    obj = ClubBase()

    # a_login_actual = LoginBase().login(do_config("username", "A"))
    # a_login_token = a_login_actual.json()["token"]
    a_login_token = "1"
    # time_id = obj.get_time_id(a_login_token)
    time_id = 8
    print(time_id)
    data_list = {"send_time_id": time_id}
    actual = ClubBase().club_info_update(a_login_token, 5109, data_list)
    print(actual.json())
    # actual = obj.get_clubs_info(a_login_token, 5109)
    # print(actual.json()["member_num"])
    # b_login_actual = LoginBase().login(do_config("username", "B"))
    # b_login_token = b_login_actual.json()["token"]
    # print(b_login_actual.json()["user_info"]["id"])
    # actual = obj.get_packet_detail(b_login_token, 5109)
    # print(actual.status_code)
    # print(actual.json())



