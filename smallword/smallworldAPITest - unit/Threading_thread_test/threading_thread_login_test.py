# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import random

import requests
import json
import multiprocessing
import threading
import time
import uuid
import unittest

from libs.ddt import ddt,data
from scripts.Base import Base
from scripts.activities_and_discoveries.discover_base import DiscoverBase
from scripts.constants import TEST_ONE_DATAS_USER_FILE_PATH, TEST_TWO_DATAS_USER_FILE_PATH
from scripts.handle_config import do_config
from scripts.logins.login_base import LoginBase

login_one_data_list = Base().read_user(TEST_ONE_DATAS_USER_FILE_PATH)
login_two_data_list = Base().read_user(TEST_TWO_DATAS_USER_FILE_PATH)

# print(login_one_data_list, type(login_one_data_list))
# print(login_two_data_list, type(login_two_data_list))

def login(phone="17621620738", password="a123456"):
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
    send_res = requests.Session()
    actual = send_res.post(method="post", url=login_url, headers=headers, json=data)
    send_res.close()
    return actual.json()["token"]


try:
    i = 0
    # t1, t2, t3, t4 = [], [], [], []
    # 开启线程数目
    tasks_number = 10
    print('测试启动')
    time1 = time.clock()
    while i < tasks_number:
        t1 = threading.Thread(target=login)
        t1.start()
        t1.join()
        i += 1

    time2 = time.clock()
    times = time2 - time1
    print(times)
    print(times/tasks_number)

except Exception as e:
    print(e)


