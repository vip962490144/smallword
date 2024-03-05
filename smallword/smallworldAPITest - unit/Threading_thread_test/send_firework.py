from multiprocessing import Pool
import time, random, os

import requests

from scripts.Base import Base
from scripts.constants import TEST_USER_DATAS_USER_FILE_PATH
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest

# 登录
from scripts.user_info.user_base import UserBase


def login(phone="17621620001", password="a123456"):
    # 返回登录的token
    headers = {'content-type':'application/json', 'authorization': 'Bearer '}
    login_url = do_config("api", "url") + "users/login"
    # print("手机号{}".format(phone))
    data = {"mobile":phone,
            "password": password,
            "device": "android",
            "language": "ch",
            "area_code": "+86",
            "device_no": "test",
            "phone_type": "9500",
            "system": "28",
            "idfa": "test"}
    one_session = requests.Session()
    actual = one_session.post(url=login_url, headers=headers, json=data)
    one_session.close()
    return actual.json()["token"]


def send_firework(token):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    # url = "http://106.75.29.100:8081/" + "redPacket/send_firework"
    url = do_config("api", "url") + "redPacket/send_firework"
    data = {"num": 1}   # 红包个数
    one_session = requests.Session()
    actual = one_session.post(url=url, json=data, headers=headers)
    one_session.close()
    return actual

def foo(info):
    print(info)     # 传入值为进程执行结果


if __name__ == '__main__':
    login_one_data_list = Base().read_user(TEST_USER_DATAS_USER_FILE_PATH)
    list_token = []
    for i in range(100):    # 发红包的人数
        login_data = login_one_data_list[i]
        phone = login_data["mobile"]
        password = login_data["password"]

        token = login(phone, password)
        list_token.append(token)
    for var in list_token:
        time.sleep(0.8)  # 时间，0.8秒
        actual = send_firework(var)
        print(actual.text)
