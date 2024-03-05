import json
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
    send_res = HandleRequest()
    actual = send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
    send_res.close()
    return actual.json()["token"]


# 获取验证码
def captcha(mobile):
    headers = {'content-type':'application/json', 'authorization': 'Bearer '}
    login_url = do_config("api", "url") + "users/captcha"

    data = {"mobile": mobile, "type": "4", "area_code": "+86", "language": "zh"}
    send_res = HandleRequest()
    actual = send_res(method="POST", url=login_url, headers=headers, data=data, is_json=True)
    send_res.close()
    return actual


# 注册
def register(mobile):
    headers = {'content-type':'application/json', 'authorization': 'Bearer '}
    login_url = do_config("api", "url") + "users/verify_code"
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


# 后台登录
def backend_login(login_data):
    # 返回登录的token
    headers = {'content-type': 'application/json', 'authorization': 'Bearer '}
    data_list = json.loads(login_data)

    login_url = do_config("api", "url") + "backend/admins/login"
    account = data_list["account"]
    password = data_list["password"]

    data = {"account": account, "password": password}

    send_res = HandleRequest()
    actual = send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
    send_res.close()
    return actual


# 后台审核聚会
def check_party(login_token, party_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
    end_url = do_config("api", "url") + "backend/party/check"
    """
    |party_id|YES|聚会id|
    |result|Yes|审核结果 1 通过；-1 拒绝|
    |reason|No|拒绝理由|
    |modify_id|No|修改id，审核status为2时必传|
    """
    data_list = {"party_id": party_id, "result": 1}
    send_res = HandleRequest()
    actual = send_res(method="post", url=end_url, data=data_list, headers=headers, is_json=True)
    send_res.close()

    return actual


# 参加聚会
def apply_for_party(login_token, party_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
    apply_panty_url = do_config("api", "url") + "party/apply"
    data_list = {"party_id": party_id, "be_present_flag": 1, "airline_ticket_flag": 1,
                 "hotel_flag": 1, "remarks": "想参加"}
    send_res = HandleRequest()
    actual = send_res(method="post", url=apply_panty_url, data=data_list, headers=headers, is_json=True)
    send_res.close()

    return actual


# 同意他人加入聚会的申请
def handle_apply(login_token, apply_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
    apply_panty_url = do_config("api", "url") + "party/applications/{}".format(apply_id)
    send_res = HandleRequest()
    actual = send_res(method="put", url=apply_panty_url, headers=headers, is_json=True)
    send_res.close()

    return actual


# 发布聚会
def create_party(login_token):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
    create_panty_url = do_config("api", "url") + "party"
    time_num = int(time.time()) + 43200
    data_list = {"name": "纯high聚会1", "appoint_time": time_num, "city": "上海",
                 "location": "漕宝路650号", "location_uid": "11122311",
                 "num": 2, "packet_money": 10000, "ticket_hotel_flag": 1,
                 "description": "赶快进来high", "address": "上海徐汇区", "type": 1,
                 "flag_anonymous": 0, "merchant_id": 1}

    send_res = HandleRequest()
    actual = send_res(method="post", url=create_panty_url, data=data_list, headers=headers, is_json=True)
    send_res.close()

    return actual


# 发聚会红包
def send_party_packet(login_token, party_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token,
               "app-version": "2.9.15"}
    url = do_config("api", "url") + "party/packet"
    data = {"party_id": party_id}
    res = HandleRequest()
    actual = res(method="post", url=url, data=data, headers=headers, is_json=True)
    res.close()
    return actual


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
    print(info)  # 传入值为进程执行结果


# 聚会签到
def party_signup(token, party_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
               "app-version": "2.9.15"}
    url = do_config("api", "url") + "/party/signup"
    # data_list = {"party_id": party_id, "lat": "31.16237", "lon": "121.405222"}
    data_list = {"party_id": party_id, "lat": "3.16237", "lon": "1.405222"}
    send_res = HandleRequest()
    actual = send_res(method="POST", url=url, data=data_list, headers=headers, is_json=True)
    send_res.close()

    return actual


# 修改聚会信息
def update_party_info(token, data, party_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    url = do_config("api", "url") + "party/{}".format(party_id)
    send_res = HandleRequest()
    actual = send_res(method="put", url=url, data=data, headers=headers, is_json=True)
    send_res.close()

    return actual


# 修改用户经纬度
def put_users_location(token):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    url = do_config("api", "url") + "/users/location"
    # data_list = {"longitude": "121.405222", "latitude": "31.16237"}
    data_list = {"longitude": "3.16237", "latitude": "1.405222"}
    send_res = HandleRequest()
    actual = send_res(method="put", url=url, data=data_list, headers=headers, is_json=True)
    send_res.close()

    return actual


# 获取聚会的经纬度地址
def get_party_location(tokne, party_id):
    pass


if __name__ == '__main__':
    login_one_data_list = Base().read_user(TEST_USER_DATAS_USER_FILE_PATH)

    token = login("17621620738", "123456")
    # captcha("15224983103")
    # actual = register("15224983103")
    # token = actual.json()["token"]
    actual = create_party(token)
    party_id = actual.json()["id"]
    # party_id = 8313
    # print(party_id)

    actual = backend_login(do_config("admin", "A"))
    token = actual.json()["token"]
    check_party(token, party_id)

    p = Pool(10)
    li = []
    t4 = 0
    list_token = []
    apply_id_list = []
    for i in range(20):
        login_data = login_one_data_list[i]
        phone = login_data["mobile"]
        password = login_data["password"]
        token = login(phone, password)
        actual = apply_for_party(token, party_id)
        apply_id = actual.json()["id"]
        apply_id_list.append(apply_id)
        list_token.append(token)

    # redpacket_id = "997878"

    token = login("17621620738", "123456")
    for i in apply_id_list:
        handle_apply(token, i)
    # captcha("15224983103")
    # actual = register("15224983103")
    # token = actual.json()["token"]

    data_list2 = {"appoint_time": 0}
    put_users_location(token)
    update_party_info(token, data_list2, party_id)
    #
    time.sleep(70)
    actual = party_signup(token, party_id)
    print(actual.text)
    redpacket_actual = send_party_packet(token, party_id)
    # print(redpacket_actual.text)
    redpacket_id = redpacket_actual.json()["id"]

    token_list = []
    for var in list_token:
        # put_users_location(var)
        # party_signup(var, party_id)
        t1 = time.time()
        # 领取红包
        # res = receive_redpacket(var, redpacket_id)
        # res = p.apply_async(receive_redpacket, args=(var, redpacket_id),
        #                     callback=foo)
        # 结果不会立刻返回，遇到阻塞，开启下一个进程，在这，
        # 相当于几乎同时出现8个打印结果（一个线程处理一个任务，处理完下个任务才能进来）
        # li.append(res)
        t2 = time.time()
        t3 = t2 - t1
        t4 += t3

    p.close()  # join之前需要关闭进程池
    p.join()  # 因为异步，所以需要等待池内进程工作结束再继续
    for i in li:
        print(i)
        # print(i.get())  # i是一个对象，通过get方法获取返回值，而同步则没有该方法
    print("总耗时：{}".format(t4))
