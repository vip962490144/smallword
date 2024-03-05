# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import json
import time

from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase


def send_redpacket(login_token, data_list):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
    club_redpacket_url = do_config("api", "url") + "clubs/packet"
    # data_list = {"club_id":"1846","user_num":"3","total_money":"102","memo":"美女才可以领"}
    send_res = HandleRequest()
    actual = send_res(method="post", url=club_redpacket_url, data=data_list, headers=headers, is_json=True)
    send_res.close()

    return actual


def login(login_data):
        # 返回登录的token
    headers = {'content-type':'application/json', 'authorization': 'Bearer ',
               "app-version": "2.33.0"}
    # data_list = json.loads(login_data)
    # print(type(data_list))
    login_url = do_config("api", "url") + "users/login"
    # login_url = "http://106.75.29.100:8081/" + "users/login"
    mobile = login_data["mobile"]
    password = login_data["password"]
    data = {"mobile": mobile,"password": password,
            "device": "android","language": "ch",
            "area_code": "+86","device_no": "test",
            "phone_type": "9500","system": "28","idfa": "test"}
    send_res = HandleRequest()
    actual = send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
    send_res.close()
    return actual


login_data = {"mobile": "18360830002", "password": "123456"}
login_data1 = {"mobile": "17621620720", "password": "123456"}

login_token1 = login(login_data).json()["token"]
# user_info = login(login_data).json()["user_info"]
print(login_token1)
# print(user_info)

login_token = login(login_data1).json()["token"]
# user_info = login(login_data1).json()["user_info"]
print(login_token)
# print(user_info)

data_list = {"club_id":"12749","user_num":"3","total_money":"102","memo":"美女才可以领"}

send_redpacket(login_token, data_list)

# for a in range(1000):
#     time.sleep(3)
#     actual = send_redpacket(login_token1, data_list)
#     print(actual.status_code)
