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


# 随机获得点赞数和用户的视频id
def random_mun():
    # data_list = 2408 - 2507
    # submit_id = random.choice(data_list)
    submit_id = random.randint(2408, 2507)
    submit_like_num = random.randint(50, 98)
    return submit_id,submit_like_num


# 一对多进行点赞
def OneSubmitLike():
    login_actual = LoginBase().login(do_config("username", "C"))
    login_token = login_actual.json()["token"]
    for i in range(0, 10):
        submit_id,submit_like_num = random_mun()
        data_list = {"submit_id": submit_id,'like_num': submit_like_num}

        try:
            submit_actual = DiscoverBase().submit_like(login_token, data_list)
            submit_text = submit_actual.json()
        except:
            print("点赞失败", submit_actual, login_actual.json()["user_info"]["id"])
        else:
            print("点赞成功，剩余钻石：{}".format(submit_text))

# 一对一进行点赞
def OnetoOneSubmitLike(one_to_one_data):
    login_actual = LoginBase().login(do_config("username", "A"))
    login_token = login_actual.json()["token"]
    for i in range(0, 10):
        submit_id,submit_like_num = random_mun()
        data_list = {"submit_id": one_to_one_data, 'like_num': submit_like_num}

        try:
            submit_actual = DiscoverBase().submit_like(login_token, data_list)
            submit_text = submit_actual.json()
        except:
            print("点赞失败", submit_actual, login_actual.json()["user_info"]["id"])
        else:
            print("点赞成功，剩余钻石：{}".format(submit_text))


# 一对一进行点赞
def OneToOneSubmitLike(one_to_one_data):
    login_actual = LoginBase().login(do_config("username", "B"))
    login_token = login_actual.json()["token"]
    for i in range(0, 10):
        submit_id, submit_like_num = random_mun()
        data_list = {"submit_id": one_to_one_data,'like_num': submit_like_num}

        try:
            submit_actual = DiscoverBase().submit_like(login_token, data_list)
            submit_text = submit_actual.json()
        except:
            print("点赞失败", submit_actual, login_actual.json()["user_info"]["id"])
        else:
            print("点赞成功，剩余钻石：{}".format(submit_text))



# 多对多进行点赞
def MoreSubmitLike(login_data):
    login_data = json.dumps(login_data)
    login_actual = LoginBase().login(login_data)
    login_token = login_actual.json()["token"]
    submit_id,submit_like_num = random_mun()
    data_list = {"submit_id": submit_id,'like_num': submit_like_num}

    try:
        submit_actual = DiscoverBase().submit_like(login_token, data_list)
        submit_text = submit_actual.json()
    except:
        print("点赞失败", submit_actual, login_actual.json()["user_info"]["id"])
    else:
        print("点赞成功，剩余钻石：{}".format(submit_text))


# 多对一进行点赞
def DoubleSubmitLike(login_data, submit_id, submit_like_num):
    login_data = json.dumps(login_data)
    login_actual = LoginBase().login(login_data)
    login_token = login_actual.json()["token"]
    data_list = {"submit_id": submit_id, 'like_num': submit_like_num}

    try:
        submit_actual = DiscoverBase().submit_like(login_token, data_list)
        submit_text = submit_actual.json()
    except:
        print("点赞失败", submit_actual, login_actual.json()["user_info"]["id"])
    else:
        print("点赞成功，剩余钻石：{}".format(submit_text))


def for_login_double():
    submit_id,submit_like_num = random_mun()
    for value in range(0, len(login_one_data_list)):
        login_data = login_one_data_list[value]
        actual = DoubleSubmitLike(login_data, submit_id, submit_like_num)


def for_login_more():
    # data_list = json.dumps(login_data_list)
    for value in range(0, len(login_two_data_list)):
        login_data = login_two_data_list[value]
        # print(login_data)
        actual = MoreSubmitLike(login_data)


def one_more():
    one_actual = OneSubmitLike()
    # return one_actual


def more_more():
    more_actual = for_login_more()
    # return more_actual


def more_one():
    more_one_actual = for_login_double()
    # return more_one_actual


def one_to_one(one_to_one_data1, one_to_one_data2):
    one_To_one_actual = OneToOneSubmitLike(one_to_one_data1)
    one_to_one_actual = OnetoOneSubmitLike(one_to_one_data2)

# def one_To_one(one_to_one_data2):
#     one_to_one_actual = OnetoOneSubmitLike(one_to_one_data2)


# one_more()
# more_more()
# more_one()
# one_to_one_data = ["1682", "1688"]
# one_to_one(one_to_one_data[0], one_to_one_data[1])
# one_To_one(one_to_one_data[1])


try:
    i = 0
    # t1, t2, t3, t4 = [], [], [], []
    # 开启线程数目
    tasks_number = 10
    print('测试启动')
    time1 = time.clock()
    while i < tasks_number:
        t1 = threading.Thread(target=one_more)
        t2 = threading.Thread(target=more_more)
        t3 = threading.Thread(target=more_one)
        # t4 = threading.Thread(target=one_to_one, args=(one_to_one_data[0], one_to_one_data[1]))
        # t4 = multiprocessing.Process(target=one_to_one, args=(one_to_one_data[0], one_to_one_data[1]))

        t1.start()
        t2.start()
        t3.start()
        # t4.start()
        t1.join()
        t2.join()
        t3.join()
        # t4.join()
        i += 1

    time2 = time.clock()
    times = time2 - time1
    print(times)
    print(times/tasks_number)

except Exception as e:
    print(e)


