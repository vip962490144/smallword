from multiprocessing import Pool
import time, random, os

import requests

from scripts.Base import Base
from scripts.constants import TEST_USER_DATAS_USER_FILE_PATH
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest

# def func(n):
#     pid = os.getpid()
#     print('进程%s正在处理第%d个任务'%(pid,n),'时间%s'%time.strftime('%H-%M-%S'))
#     time.sleep(2)
#     res = '处理%s'%random.choice(['成功','失败'])
#     return res


# 登录
from scripts.redpackets.redpacket_base import RedpacketBase


def login(phone="17621620001", password="a123456"):
    # 返回登录的token
    headers = {'content-type': 'application/json', 'authorization': 'Bearer '}
    login_url = do_config("api", "url") + "users/login"
    # print("手机号{}".format(phone))
    data = {"mobile": phone,
            "password": password,
            "device": "android",
            "language": "ch",
            "area_code": "+86",
            "device_no": "test",
            "phone_type": "9500",
            "system": "28",
            "idfa": "test"}
    # send_res = HandleRequest()
    one_session = requests.Session()
    # actual = send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
    actual = one_session.post(url=login_url, headers=headers, json=data)
    one_session.close()
    return actual


# 创建礼物红包
def create_raffle_gifts(token, sku_data, club_id=None):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    url = do_config("api", "url") + "mallProduct/create_raffle_gifts"
    if club_id is None:
        data = {"note": "dolor",
                "sku_data": sku_data
                }
    else:
        data = {"note": "dolor", "club_id": club_id,
                "sku_data": sku_data
                }
    one_session = requests.Session()
    actual = one_session.post(url=url, headers=headers, json=data)
    one_session.close()
    # res = HandleRequest()
    # actual = res(method="post", url=url, data=data, headers=headers, is_json=True)
    # res.close()
    return actual


# 礼物红包支付
def pay_raffle_gift_order(token, gift_draw_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    url = do_config("api", "url") + "charge/pay_raffle_gift_order"
    data = {"gift_draw_id": gift_draw_id}
    one_session = requests.Session()
    actual = one_session.post(url=url, headers=headers, json=data)
    one_session.close()
    # res = HandleRequest()
    # actual = res(method="post", url=url, data=data, headers=headers, is_json=True)
    # res.close()
    return actual


# 领取红包进行抽奖
def lucky_draw(token, gift_draw_id, id=None):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    url = do_config("api", "url") + "mallProduct/initiate_lucky_draw"
    data = {"gift_draw_id": gift_draw_id}
    one_session = requests.Session()
    actual = one_session.post(url=url, headers=headers, json=data)
    one_session.close()
    # res = HandleRequest()
    # actual = res(method="post", url=url, data=data, headers=headers, is_json=True)
    # res.close()
    # print(id)
    return actual.json()


def foo(info):
    print(info)  # 传入值为进程执行结果


if __name__ == '__main__':
    login_one_data_list = Base().read_user(TEST_USER_DATAS_USER_FILE_PATH)
    p = Pool(10)
    li = []
    t4 = 0
    #
    # list_token = []
    # list_id = []
    # for var in range(20):
    #     login_data = login_one_data_list[var]
    #     phone = login_data["mobile"]
    #     password = login_data["password"]
    #     t1 = time.time()
    #     # 领取红包
    #     res = p.apply_async(login, args=(phone, password))
    #     # 结果不会立刻返回，遇到阻塞，开启下一个进程，在这，
    #     # 相当于几乎同时出现8个打印结果（一个线程处理一个任务，处理完下个任务才能进来）
    #     li.append(res)
    #     token = res
    #     list_token.append(token)
    #     t2 = time.time()
    #     t3 = t2 - t1
    #     t4 += t3
    #
    # p.close()  # join之前需要关闭进程池
    # p.join()  # 因为异步，所以需要等待池内进程工作结束再继续
    # for i in li:
    #     print(i.get())  # i是一个对象，通过get方法获取返回值，而同步则没有该方法
    # print("总耗时：{}".format(t4))

    list_token = []
    list_id = []
    # 读取人数
    for i in range(500):
        login_data = login_one_data_list[i]
        phone = login_data["mobile"]
        password = login_data["password"]
        actual = login(phone, password)
        token = actual.json()["token"]
        id = actual.json()["user_info"]["id"]
        list_id.append(id)
        list_token.append(token)

    actual = login("17621620738", "123456")
    token = actual.json()["token"]
    # token = actual
    sku_data = RedpacketBase().get_sku_data(token)
    redpacket_actual = create_raffle_gifts(token, sku_data)
    print(redpacket_actual.json())
    gift_draw_id = redpacket_actual.json()["gift_draw_id"]
    actual = pay_raffle_gift_order(token, gift_draw_id)
    print(actual.json())
    # redpacket_id = "997878"
    p = Pool(20)
    li = []
    t4 = 0

    for var in range(len(list_token)):
        # login_data = login_one_data_list[var]
        # phone = login_data["mobile"]
        # password = login_data["password"]
        t1 = time.time()
        # 登录
        # res1 = p.apply_async(login, args=(phone, password))
        # 领取红包
        res = p.apply_async(lucky_draw, args=(list_token[var], gift_draw_id),
                            callback=foo)
        # 结果不会立刻返回，遇到阻塞，开启下一个进程，在这，
        # 相当于几乎同时出现8个打印结果（一个线程处理一个任务，处理完下个任务才能进来）
        li.append(res)
        t2 = time.time()
        t3 = t2 - t1
        t4 += t3

    p.close()  # join之前需要关闭进程池
    p.join()  # 因为异步，所以需要等待池内进程工作结束再继续
    for i in li:
        print(i.get())  # i是一个对象，通过get方法获取返回值，而同步则没有该方法
    print("总耗时：{}".format(t4))
