# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import time
import os
from multiprocessing import Pool
import time, random, os

from scripts.Base import Base
from scripts.constants import TEST_USER_DATAS_USER_FILE_PATH
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest

from scripts.constants import CONFIGS_DIR
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest


def captcha(mobile):
    headers = {'content-type':'application/json', 'authorization': 'Bearer ', "app-version": "2.11.2"}
    login_url = do_config("api", "url") + "users/captcha"
    # login_url = "http://stress-api.onemicroworld.com/" + "users/captcha"

    # login_url = "http://106.75.29.100:8081/" + "users/captcha"

    data = {"mobile": mobile, "type": "4", "area_code": "+86", "language": "zh"}
    send_res = HandleRequest()
    actual = send_res(method="POST", url=login_url, headers=headers, data=data, is_json=True)
    send_res.close()
    return actual

# 注册
def register(mobile):
    headers = {'content-type':'application/json', 'authorization': 'Bearer ', "app-version": "2.11.2"}
    login_url = do_config("api", "url") + "users/verify_code"
    # login_url = "http://stress-api.onemicroworld.com/" + "users/verify_code"
    # login_url = "http://106.75.29.100:8081/" + "users/verify_code"
    data = {"mobile": mobile,
            "flag_old_invite":"1",
            "password":"123456",
            "device":"android",
            "language":"ch",
            "area_code":"+86",
            "captcha":"0000",
            "device_no":"test",
            "idfa":"test"
            }
    # data = {"mobile": 17621620900, "captcha": "0000", "password": "123456", "device": "android"}
    send_res = HandleRequest()
    actual = send_res(method="POST", url=login_url, headers=headers, data=data, is_json=True)
    send_res.close()
    return actual


def write_config(token):
    """
    将数据写入配置文件
    :return:
    """
    boy_text = os.path.join(CONFIGS_DIR, "user_1w.txt")
    with open(boy_text, 'a') as boy:
        boy.write(str(token)+',\n')

def foo(info):
    print(info)


if __name__ == '__main__':

    mobile = 13520010000
    columns = ["mobile"]
    # captcha(mobile)
    # actual = register(mobile)
    # print(actual.text)
    list_token = []
    for var in range(10000):
        # write_config(mobile)
        captcha(mobile)
        actual = register(mobile)
        # print(actual.json())
        token = actual.json()["token"]
        # list_a = [mobile]
        list_token.append(token)
        mobile += 1

    # p = Pool(40)
    # li = []
    # t4 = 0

    for var in list_token:
        write_config(var)
    #     t1 = time.time()
    #     # 领取红包
    #     res = p.apply_async(write_config, args=(var),
    #                         callback=foo)
    #     # 结果不会立刻返回，遇到阻塞，开启下一个进程，在这，
    #     # 相当于几乎同时出现8个打印结果（一个线程处理一个任务，处理完下个任务才能进来）
    #     li.append(res)
    #     t2 = time.time()
    #     t3 = t2-t1
    #     t4 += t3
    #
    # p.close()   # join之前需要关闭进程池
    # p.join()    # 因为异步，所以需要等待池内进程工作结束再继续
    # for i in li:
    #     print(i.get())  # i是一个对象，通过get方法获取返回值，而同步则没有该方法
    # print("总耗时：{}".format(t4))
