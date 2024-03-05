from multiprocessing import Pool
import time, random, os

# from scripts.Base import Base
from scripts.constants import TEST_USER_DATAS_USER_FILE_PATH, TEST_USER_DATAS_USER8_FILE_PATH
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest


# def func(n):
#     pid = os.getpid()
#     print('进程%s正在处理第%d个任务'%(pid,n),'时间%s'%time.strftime('%H-%M-%S'))
#     time.sleep(2)
#     res = '处理%s'%random.choice(['成功','失败'])
#     return res


# 获取验证码
def captcha(mobile):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer '}
    login_url = do_config("api", "url") + "users/captcha"
    # login_url = "http://106.75.29.100:8081/" + "users/captcha"

    data = {"mobile": mobile, "type": "4", "area_code": "+86", "language": "zh"}
    send_res = HandleRequest()
    actual = send_res(method="POST", url=login_url, headers=headers, data=data, is_json=True)
    send_res.close()
    return actual


# 注册
def register(mobile):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer '}
    login_url = do_config("api", "url") + "users/verify_code"
    # login_url = "http://106.75.29.100:8081/" + "users/verify_code"
    data = {"mobile": mobile,
            "flag_old_invite": "1",
            "password": "123456",
            "device": "android",
            "language": "ch",
            "area_code": "+86",
            "captcha": "0000",
            "device_no": "test",
            "idfa": "test"
            }
    # data = {"mobile": 17621620900, "captcha": "0000", "password": "123456", "device": "android"}
    send_res = HandleRequest()
    actual = send_res(method="POST", url=login_url, headers=headers, data=data, is_json=True)
    send_res.close()
    return actual


# 登录
def login(phone="17621620001", password="a123456"):
    # 返回登录的token
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ',
               "app-version": "2.47.0"}
    login_url = do_config("api", "url") + "users/login"
    # print("手机号{}".format(phone))
    data = {"mobile": phone,
            "password": password,
            "device": "android",
            "language": "ch",
            "area_code": "+86",
            "device_no": "1e289035937c21e7",
            "phone_type": "OnePlusHD1910",
            "system": "11",
            "idfa": "1e289035937c21e7"}
    send_res = HandleRequest()
    actual = send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
    send_res.close()
    return actual


def send_gift(login_token, send_data):
    send_url = do_config("api", "url") + "gifts/send2"
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
    # 创建会话
    send_res = HandleRequest()
    actual = send_res(method="post", url=send_url, headers=headers, data=send_data, is_json=True)
    send_res.close()
    return actual


def friends_apply_list(token, pos_num, limit_num):
    url = do_config("api", "url") + "chat/message?pos={}&limit={}&flag_type=3".format(pos_num, limit_num)
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
               "app-version": "2.47.0"}
    send_res = HandleRequest()
    actual = send_res(method="get", url=url, headers=headers)
    send_res.close()
    return actual


# 接受好友请求
def friends_apply(token, apply_id):
    url = do_config("api", "url") + "friends/apply"
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
               "app-version": "2.47.0"
               }
    # apply_id = str(apply_id)
    data = {"id": apply_id, "result": "1"}
    send_res = HandleRequest()
    actual = send_res(method="put", url=url, data=data, headers=headers, is_json=True)
    send_res.close()
    return actual


def read_user(username):
    """
    :param username: 文件名，绝对路径
    :return:
    """
    with open(username, "r") as file:
        data_list = []
        while True:
            mystr = file.readline().strip('\n')  # 表示一次读取一行
            my_user = mystr.split(",")
            if not mystr:
                # 读到数据最后跳出，结束循环。数据的最后也就是读不到数据了，mystr为空的时候
                return data_list
            mobile, password = my_user[0], my_user[1]
            data = {"mobile": mobile, "password": password}
            data_list.append(data)


def foo(info):
    print(info)  # 传入值为进程执行结果


if __name__ == '__main__':
    # t0 = time.time()
    # print(t0)
    # login_one_data_list = read_user(TEST_USER_DATAS_USER_FILE_PATH)
    # # print(login_one_data_list)
    # p = Pool(10)
    # li = []
    # t4 = 0
    # list_token = []
    # for i in range(300, 5000):
    #     login_data = login_one_data_list[i]
    #     phone = login_data["mobile"]
    #     password = login_data["password"]
    #     actual = login(phone, password)
    #     # captcha(phone)
    #     # actual = register(phone)
    #     try:
    #         # print(actual.json())
    #         token = actual.json()["token"]
    #     except Exception as e:
    #         pass
    #     else:
    #         list_token.append(token)
    mobile = 12345678906
    captcha(mobile)
    res = register(mobile)
    user_token = res.json()["token"]
    user_id = res.json()["user_info"]["id"]
    # token = login("17621620738", "123456")

    # send_data = {"gift_id": 303, "receiver_id": user_id, "apply_content": "mmmm",
    #              "flag_apply": 1, "num": 1, "private_flag": 0, "source": 1}
    # print(len(list_token))
    # for var in list_token:
    #     t1 = time.time()
    #     # 领取红包
    #     res = p.apply_async(send_gift, args=(var, send_data))
    #     # 结果不会立刻返回，遇到阻塞，开启下一个进程，在这，
    #     # 相当于几乎同时出现8个打印结果（一个线程处理一个任务，处理完下个任务才能进来）
    #     # li.append(res)
    #     t2 = time.time()
    #     t3 = t2 - t1
    #     t4 += t3
    # t5 = t0 + t4
    # p.close()  # join之前需要关闭进程池
    # p.join()  # 因为异步，所以需要等待池内进程工作结束再继续
    # # for i in li:
    # # print(i.get())  # i是一个对象，通过get方法获取返回值，而同步则没有该方法
    # print("总耗时：{}".format(t5))

    # print(res.get())

    pos_num = 0
    limit_num = 10
    # user_token = "68e826145212b5c36e182f9b247335c5"
    apply_friend_id_list = []
    for var in range(0, 500):
        actual = friends_apply_list(user_token, pos_num, limit_num)
        apply_list = actual.json()["list"]
        for i in apply_list:
            friend_status = int(i["friend_status"])
            if friend_status == 0:
                apply_id = i["apply_friend_id"]
                # print(apply_id)
                apply_friend_id_list.append(apply_id)
        pos_num += 10

    print(len(apply_friend_id_list))

    for var in range(len(apply_friend_id_list)):
        # first_apply = friend_first_apply(user_token)
        res = friends_apply(user_token, apply_friend_id_list[var])
    print(res.json())

    t6 = time.time()
    print(t6)
