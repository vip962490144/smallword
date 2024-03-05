# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import datetime
import random
import time

from scripts.clubs.club_base import ClubBase
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase
from scripts.partys.party_base import PartyBase


def equal_clubs():
    login_actual = LoginBase().login(do_config("username", "A"))
    login_token = login_actual.json()["token"]

    my_create_clubs_list, my_join_clubs_list = ClubBase().get_clubs_list(login_token)
    # print(my_create_clubs_list)
    club_list1 = []
    for i in range(len(my_join_clubs_list)):
        var = my_join_clubs_list[i]["id"]
        club_list1.append(var)
    # print(club_list1)

    party_list1 = []
    for i in range(len(my_create_clubs_list)):
        var = my_create_clubs_list[i]["id"]
        party_list1.append(var)

    # print(party_list1)


# 获取俱乐部详情
def get_clubs_info(login_token, club_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
    clubs_url = do_config("api", "url") + "/clubs/info?club_id={}".format(club_id)
    send_res = HandleRequest()
    actual = send_res(method="get", url=clubs_url, headers=headers)
    send_res.close()

    return actual


# 修改俱乐部信息
def club_info_update(login_token, club_id, data_list):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
    clubs_url = do_config("api", "url") + "/clubs/{}".format(club_id)
    send_res = HandleRequest()
    actual = send_res(method="PUT", url=clubs_url, data=data_list, headers=headers, is_json=True)
    send_res.close()

    return actual


# 获取俱乐部红包时间列表
def club_packet_time_list(login_token):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
    clubs_url = do_config("api", "url") + "/clubs/send_time"
    send_res = HandleRequest()
    actual = send_res(method="GET", url=clubs_url, headers=headers)
    send_res.close()

    return actual


equal_clubs()

login_actual = LoginBase().login(do_config("username", "A"))
login_token = login_actual.json()["token"]

actual = get_clubs_info(login_token, 5109)
print(actual.json())

time_id = ClubBase().get_time_id(login_token)

data_list = {"name": "红红火火恍恍惚惚", "gender_limit": 3,
             "send_time_id": time_id, "packet_money": 30,
             "packet_diamond": 4, "notice": "红红火火恍恍惚惚", "flag_chat": 1}

actual = club_info_update(login_token, 5109, data_list)
print(actual.json())
