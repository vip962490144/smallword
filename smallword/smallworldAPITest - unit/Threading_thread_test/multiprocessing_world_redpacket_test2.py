from multiprocessing import Pool
import time, random, os

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
    send_res = HandleRequest()
    actual = send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
    send_res.close()
    return actual.json()["token"]


def send_world_redpacket(login_token):
    # 发送红包
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
    data_list = {"type": 3, "user_num": "300", "total_money": 5000, "memo": "新年快乐"}
    club_redpacket_url = do_config("api", "url") + "clubs/packet"
    send_res = HandleRequest()
    actual = send_res(method="post", url=club_redpacket_url, data=data_list, headers=headers, is_json=True)
    send_res.close()

    return actual.json()["id"]


# 领取红包
def receive_redpacket(login_token, redpacket_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
    club_redpacket_url = do_config("api", "url") + "clubs/packet/" + redpacket_id
    send_res = HandleRequest()
    # actual = send_res(method="put", url=club_redpacket_url, headers=headers, is_json=True)
    actual2 = send_res(method="put", url=club_redpacket_url, headers=headers, is_json=True)
    send_res.close()
    # print(actual.json())
    return actual2.json()


def foo(info):
    print(info)     # 传入值为进程执行结果


if __name__ == '__main__':
    login_one_data_list = Base().read_user(TEST_USER_DATAS_USER_FILE_PATH)
    p = Pool(100)
    li = []
    t4 = 0
    user_info_after = []
    list_token = []
    user_info_dict = []
    for i in range(300):
        login_data = login_one_data_list[i]
        phone = login_data["mobile"]
        password = login_data["password"]

        token = login(phone, password)
        list_token.append(token)

    token = login("17621620032", "a123456")
    redpacket_id = send_world_redpacket(token)
    # redpacket_id = "997878"

    for var in list_token:
        t1 = time.time()
        # 领取红包
        res = p.apply_async(receive_redpacket, args=(var, redpacket_id),
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
