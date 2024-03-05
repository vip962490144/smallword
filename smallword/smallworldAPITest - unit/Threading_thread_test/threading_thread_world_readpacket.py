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
from scripts.constants import TEST_ONE_DATAS_USER_FILE_PATH, TEST_TWO_DATAS_USER_FILE_PATH
from scripts.handle_config import do_config


# login_one_data_list = Base().read_user(TEST_ONE_DATAS_USER_FILE_PATH)
# login_two_data_list = Base().read_user(TEST_TWO_DATAS_USER_FILE_PATH)


# 随机获得点赞数和用户的视频id
def random_mun():
    data_list1 = ["想你", "么么哒", "生日快乐", "圣诞", "红红火火"]
    data_list3 = ["新年快乐", "吉星高照", "福星高照", "圣诞", "红红火火"]
    data_list2 = [6666, 8888, 66666, 88888, 1314, 5200, 5210]
    memo = random.choice(data_list3)
    total_money = random.choice(data_list2)
    # submit_like_num = random.randint(50, 98)
    return memo, total_money


def send_world_redpacket(total_money, memo):
    a_login_actual = Base().login(do_config("username", "A"))
    a_login_token = a_login_actual.json()["token"]
    # 发送红包
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + a_login_token}
    data_list = {"type":"3","user_num":"100","total_money": total_money,"memo": memo}
    redpacket_actual = Base().send_redpacket(a_login_token, data_list)
    print(redpacket_actual.json())

def send_packet():
    memo, total_money = random_mun()
    send_world_redpacket(total_money, memo)


try:
    print('测试启动')
    time1 = time.clock()
    print("启动时间：", time.time())
    for i in range(10):
        t_sing = threading.Thread(target=send_packet)
        t_sing.start()
        t_sing.join()

    print("结束时间：", time.time())

except Exception as e:
    print(e)


