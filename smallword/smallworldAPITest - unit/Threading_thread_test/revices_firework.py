from multiprocessing import Pool
import time, random, os

import requests

from scripts.Base import Base
from scripts.constants import TEST_USER_DATAS_USER_FILE_PATH
from scripts.handle_config import do_config


# 登录
from scripts.user_info.user_base import UserBase


def login(phone="17621620001", password="a123456"):
    # 返回登录的token
    headers = {'content-type':'application/json', 'authorization': 'Bearer '}
    # login_url = do_config("api", "url") + "users/login"
    login_url = "http://106.75.11.161:9082/api/" + "users/login"
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


# 发红包
def send_firework(token):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    url = "http://106.75.11.161:9082/api/" + "redPacket/send_firework"
    # url = do_config("api", "url") + "redPacket/send_firework"
    data = {"num": 1}   # 红包个数
    one_session = requests.Session()
    actual = one_session.post(url=url, json=data, headers=headers)
    one_session.close()
    return actual


# 领红包
def receive_firework(token, packet_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    url = "http://106.75.11.161:9082/api/" + "redPacket/receive_firework"
    # url = do_config("api", "url") + "redPacket/receive_firework"
    datalist = {"id": packet_id}
    one_session = requests.Session()
    actual = one_session.post(url=url, json=datalist, headers=headers)
    one_session.close()
    return actual


def read_user(username):
    """
    :param username: 文件名，绝对路径
    :return:
    """
    with open(username, "r") as file:
        data_list = []
        while True:
            mystr = file.readline().strip('\n')     # 表示一次读取一行
            my_user = mystr.split(",")
            if not mystr:
            # 读到数据最后跳出，结束循环。数据的最后也就是读不到数据了，mystr为空的时候
                return data_list
            mobile, password = my_user[0], my_user[1]
            data = {"mobile": mobile, "password": password}
            data_list.append(data)

def foo(info):
    print(info)     # 传入值为进程执行结果


if __name__ == '__main__':
    login_one_data_list = read_user("test_user_6.txt")
    p = Pool(40)    # 并发的进程数
    li = []
    t4 = 0
    list_token = []
    for i in range(100):    # 领红包的人数
        login_data = login_one_data_list[i]
        phone = login_data["mobile"]
        password = login_data["password"]

        token = login(phone, password)
        list_token.append(token)

    packet_id = 3365540     # 红包id

    for var in list_token:
        t1 = time.time()
        # 领取红包
        res = p.apply_async(receive_firework, args=(var, packet_id),
                            callback=foo)
        # 结果不会立刻返回，遇到阻塞，开启下一个进程，在这，
        # 相当于几乎同时出现8个打印结果（一个线程处理一个任务，处理完下个任务才能进来）
        li.append(res)
        t2 = time.time()
        t3 = t2-t1
        t4 += t3

    p.close()   # join之前需要关闭进程池
    p.join()    # 因为异步，所以需要等待池内进程工作结束再继续
    for i in li:
        print(i.get())  # i是一个对象，通过get方法获取返回值，而同步则没有该方法
    print("总耗时：{}".format(t4))
