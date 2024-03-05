# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import json
import requests
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config


class LoginBase:
    # 登录操作类

    # 登录
    def login(self, login_data):
        # 返回登录的token
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ',
                   "app-version": "2.47.0"}
        data_list = json.loads(login_data)
        # print(type(data_list))
        login_url = do_config("api", "url") + "users/login"
        print(login_url)
        # login_url = "http://106.75.29.100:8081/" + "users/login"
        mobile = data_list["mobile"]
        password = data_list["password"]
        data_list1 = {
            "mobile": mobile,
            "password": password,
            "device": "android",
            "language": "ch",
            "area_code": "+86",
            "captcha": "",
            "gee_auth_param": "",
            "gee_auth_type": 0,
            "device_no": "1e289035937c21e7",
            "phone_type": "OnePlusHD1910",
            "system": "11",
            "idfa": "1e289035937c21e7",
            "trackingio": {
                "deviceid": "36E114EE7DC46D4B4190FF0DEAA6C38DD9B44DB9BA6CF6EDA2E39088D4487D21",
                "idfa": "",
                "imei": "",
                "androidid": "1e289035937c21e7",
                "oaid": "36E114EE7DC46D4B4190FF0DEAA6C38DD9B44DB9BA6CF6EDA2E39088D4487D21",
                "rydevicetype": "OnePlus 7T Pro",
                "ryosversion": "11",
                "app_version": "4.17.0",
                "lib_version": "1.7.9",
                "type": 2
            },
            "track_type_id": "test"
        }
        send_res = HandleRequest()
        # one_session = requests.Session()
        # res = one_session.post(url=login_url, headers=headers, json=data_list1)
        actual = send_res(method="post", url=login_url, headers=headers, data=data_list1, is_json=True)
        send_res.close()
        # res.close()
        return actual

    # 后台登录
    def backend_login(self, login_data):
        # 返回登录的token
        headers = {'content-type': 'application/json', 'authorization': 'Bearer '}
        data_list = json.loads(login_data)

        login_url = do_config("api", "backend_url") + "backend/admins/login"
        account = data_list["account"]
        password = data_list["password"]

        data = {"account": account, "password": password}

        send_res = HandleRequest()
        actual = send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
        send_res.close()
        return actual

    # 后台登录获取token
    def get_backend_token(self, login_data):
        actual = self.backend_login(login_data)
        return actual.json()["token"]

    # 获取验证码
    def captcha(self, mobile):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ',
                   "app-version": "2.47.0"}
        login_url = do_config("api", "url") + "users/captcha"
        # login_url = "http://106.75.29.100:8081/" + "users/captcha"

        data = {"mobile": mobile, "type": "4", "area_code": "+86", "language": "zh"}
        send_res = HandleRequest()
        actual = send_res(method="POST", url=login_url, headers=headers, data=data, is_json=True)
        send_res.close()
        return actual

    # 注册
    def register(self, mobile):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ',
                   "app-version": "2.47.0"}
        login_url = do_config("api", "url") + "users/verify_code"
        # login_url = "http://106.75.29.100:8081/" + "users/verify_code"
        data = {"mobile": mobile,
                "flag_old_invite": "1",
                "password": "123456",
                "device": "android",
                "language": "ch",
                "area_code": "+86",
                "captcha": "0000",
                "device_no": "1e289035937c21e7",
                "idfa": "1e289035937c21e7"
                }
        # data = {"mobile": 17621620900, "captcha": "0000", "password": "123456", "device": "android"}
        send_res = HandleRequest()
        actual = send_res(method="POST", url=login_url, headers=headers, data=data, is_json=True)
        send_res.close()
        return actual

    # 查询手机号是否被注册
    def check_mobile(self, mobile):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ',
                   "app-version": "2.47.0"}
        url = do_config("api", "url") + "/users/check_mobile"
        data = {"mobile": mobile}
        send_res = HandleRequest()
        actual = send_res(method="POST", url=url, headers=headers, data=data, is_json=True)
        send_res.close()
        return actual

    # 查询手机号是否被注册
    def change_avatar(self):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ',
                   "app-version": "2.47.0"}
        url = do_config("api", "url") + "/change_avatar/opportunity"
        # data = {"mobile": mobile}
        send_res = HandleRequest()
        actual = send_res(method="GET", url=url, headers=headers, is_json=True)
        send_res.close()
        return actual


if __name__ == '__main__':
    obj = LoginBase()
    actual = obj.login(do_config("username", "A"))
    print(actual.json())
    user_token = actual.json()["token"]
    user_id = actual.json()["user_info"]["id"]
    print(user_token, user_id)
