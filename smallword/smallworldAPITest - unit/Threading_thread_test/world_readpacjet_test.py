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

import requests,time,json,threading,random

from scripts.handle_requests import HandleRequest




class Presstest(object):

    time_sum = 0

    def __init__(self,phone="17621620738",password="a123456", login_token=""):
        self.headers = {'content-type': 'application/json',
                        'authorization': 'Bearer ' + login_token}
        self.phone = phone
        self.password = password

    # 随机获得点赞数和用户的视频id
    def random_mun(self):
        data_list1 = ["想你", "么么哒", "生日快乐", "圣诞", "红红火火"]
        data_list3 = ["新年快乐", "吉星高照", "福星高照", "圣诞", "红红火火"]
        data_list2 = [6666, 8888, 66666, 88888, 1314, 5200, 5210]
        memo = random.choice(data_list3)
        total_money = random.choice(data_list2)
        # submit_like_num = random.randint(50, 98)
        return memo, total_money

    # 登录
    def login(self):
        # 返回登录的token
        headers = {'content-type':'application/json', 'authorization': 'Bearer '}
        # data_list = json.loads(login_data)
        # data_list = json.dumps(data_list)
        # print(data_list)

        login_url = do_config("api", "url") + "users/login"
        # mobile = data_list["mobile"]
        # password = data_list["password"]

        data = {"mobile":self.phone,
                "password": self.password,
                "device": "android",
                "language": "ch",
                "area_code": "+86",
                "device_no": "test",
                "phone_type": "9500",
                "system": "28",
                "idfa": "test"}

        # print(data)

        send_res = HandleRequest()
        actual = send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
        send_res.close()
        return actual

    def send_redpacket(self, login_token, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        club_redpacket_url = do_config("api", "url") + "clubs/packet"
        # data_list = {"club_id":"1846","user_num":"3","total_money":"102","memo":"美女才可以领"}
        send_res = HandleRequest()
        actual = send_res(method="post", url=club_redpacket_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    def send_world_redpacket(self, total_money, memo, login_token):
        # 发送红包
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        data_list = {"type":"3","user_num":"100","total_money": total_money,"memo": memo}
        club_redpacket_url = do_config("api", "url") + "clubs/packet"
        send_res = HandleRequest()
        actual = send_res(method="post", url=club_redpacket_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 领取红包
    def receive_redpacket(self, login_token, redpacket_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        club_redpacket_url = do_config("api", "url") + "clubs/packet/" + redpacket_id
        send_res = HandleRequest()
        actual = send_res(method="put", url=club_redpacket_url, headers=headers, is_json=True)
        send_res.close()

        return actual

    def send_packet(self, login_token):
        memo, total_money = self.random_mun()
        actual = self.send_world_redpacket(total_money, memo, login_token)
        return actual.json()["id"]

    def send(self):
        login_actual = self.login()
        login_token = login_actual.json()["token"]
        send_packet_actual = self.send_packet(login_token)
        self.id = send_packet_actual
        global packet_id
        packet_id = self.id

    def work(self):
        login_actual = self.login()
        login_token = login_actual.json()["token"]
        print(login_actual.json())
        receive_actual = self.receive_redpacket(login_token, packet_id)
        print(receive_actual.json())

    def testonework(self):
        ''' 一次并发处理单个任务'''
        i = 0
        while i < ONE_WORKER_NUM:
            i += 1
            self.work()
        time.sleep(LOOP_SLEEP)

    @classmethod
    def update(cls, num):
        cls.time_sum += num

    def run(self):
        '''使用多线程进程并发测试'''
        t1 = time.time()
        Threads = []

        for i in range(THREAD_NUM):
            t = threading.Thread(target=self.testonework, name="T" + str(i))
            t.setDaemon(True)
            Threads.append(t)

        for t in Threads:
            t.start()
        for t in Threads:
            t.join()
        t2 = time.time()

        print("===============压测结果===================")
        # print("URL:", self.press_url)
        print("任务数量:", THREAD_NUM, "*", ONE_WORKER_NUM, "=", THREAD_NUM * ONE_WORKER_NUM)
        print("总耗时(秒):", t2 - t1)
        t3 = t2 - t1
        self.update(t3)
        print("每次请求耗时(秒):", (t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM))
        print("每秒承载请求数:", 1 / ((t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM)))
        print("错误数量:", ERROR_NUM)


if __name__ == '__main__':

    login_one_data_list = Base().read_user(TEST_ONE_DATAS_USER_FILE_PATH)
    obj = Presstest()

    obj.send()
    time.sleep(2)

    THREAD_NUM = 1     # 并发线程总数
    ONE_WORKER_NUM = 1   # 每个线程的循环次数
    LOOP_SLEEP = 0.1    # 每次请求时间间隔(秒)
    ERROR_NUM = 0      # 出错数

    for value in range(0, len(login_one_data_list)):
        login_data = login_one_data_list[value]
        phone = login_data["mobile"]
        password = login_data["password"]

        obj = Presstest(phone=phone,password=password)
        obj.run()

    print("总耗时：{}".format(obj.time_sum))
