# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase


class UserBase:

    # 选择性别
    def users_info(self, token, data):
        headers = {'content-type':'application/json', 'authorization': 'Bearer ' + token}
        login_url = do_config("api", "url") + "users/info"

        # data = {"nickname": "自动" + i, "gender": "1", "wechat": "1111111"}
        send_res = HandleRequest()
        actual = send_res(method="put", url=login_url, headers=headers, data=data, is_json=True)
        send_res.close()
        return actual

    # 用户使用兑换码
    def invitation_code(self, token, code):
        headers = {'content-type':'application/json', 'authorization': 'Bearer ' + token}
        login_url = do_config("api", "url") + "invitation_code"
        data = {"code": code}

        send_res = HandleRequest()
        actual = send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
        send_res.close()
        return actual

    # 获取用户数据
    def get_user_info(self, login_token, params):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}

        user_info_url_end = "users/base_info?params={}".format(params)
        user_info_url = do_config("api", "url") + user_info_url_end
        send_res = HandleRequest()
        actual = send_res(method="get", url=user_info_url, headers=headers)
        send_res.close()

        return actual

    # 邀请列表-is_login = 0登录过的用户 = 1表示注册未登录
    def my_applynewlist(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        applynewlist_url = do_config("api", "url") + "introduce/applynewlist?is_login=0"
        send_res = HandleRequest()
        actual = send_res(method="get", url=applynewlist_url, headers=headers)
        send_res.close()
        return actual

    # 邀请有奖，任务列表
    def introduce_receive(self, token, id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        receive_url = do_config("api", "url") + "introduce/receive?inviter_id={}".format(id)
        send_res = HandleRequest()
        actual = send_res(method="get", url=receive_url, headers=headers)
        send_res.close()
        return actual

    # 我的邀请人
    def my_inviter(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        inviter_url = do_config("api", "url") + "introduce/inviter"
        send_res = HandleRequest()
        actual = send_res(method="get", url=inviter_url, headers=headers)
        send_res.close()
        return actual

    # 获取邀请有奖列表的用户id
    def my_applynewlist_id_list(self, token):
        actual = self.my_applynewlist(token)
        apply_list = actual.json()["list"]
        userid_list = []
        for i in range(len(apply_list)):
            var = apply_list[i]["userinfo"]["id"]
            userid_list.append(var)

        return userid_list

    # 邀请有奖-任务列表可领取的数量
    def introduce_receive_num(self, token, id):
        actual = self.introduce_receive(token, id)
        apply_list = actual.json()["list"]
        userid_list = []

        for i in range(len(apply_list)):
            var = apply_list[i]["num"]
            userid_list.append(var)

        return userid_list

    # 修改用户经纬度
    def put_users_location(self, token, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "users/location"
        # data_list = {"longitude": "3.16237", "latitude": "1.405222"}
        send_res = HandleRequest()
        actual = send_res(method="put", url=url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 选择性别
    def choice_gender(self, token, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
                   "app-version": "2.47.0"}
        url = do_config("api", "url") + "users/choice_gender"
        # data_list = {"longitude": "3.16237", "latitude": "1.405222"}
        send_res = HandleRequest()
        actual = send_res(method="post", url=url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 填写昵称
    def fill_nickname(self, token, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
                   "app-version": "2.47.0"}
        url = do_config("api", "url") + "users/fill_nickname"
        # data_list = {"longitude": "3.16237", "latitude": "1.405222"}
        send_res = HandleRequest()
        actual = send_res(method="put", url=url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual


if __name__ == '__main__':
    a_login_actual = LoginBase().login(do_config("username", "A"))
    a_login_token = a_login_actual.json()["token"]
    obj = UserBase()
    # my_apply_actual = obj.my_applynewlist_id_list(a_login_token)
    my_apply_actual = obj.my_applynewlist(a_login_token)
    print(my_apply_actual.json())
    # introduce_receive_actual = obj.introduce_receive(a_login_token, 12796)
    # introduce_receive = obj.introduce_receive_num(a_login_token, 12796)
    # print(introduce_receive_actual.json()["list"])



