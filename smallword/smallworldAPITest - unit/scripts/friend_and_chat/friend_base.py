# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import random

from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase


class FriendBase:
    # 好友操作类

    # 获取用户的好友列表
    def get_user_friends(self, login_token):
        url = do_config("api", "url") + "friends"
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers)
        send_res.close()
        return actual

    # 获取礼物列表
    def get_gift_list(self, login_token):
        gifts_list_url = do_config("api", "url") + "gifts"
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        send_res = HandleRequest()
        actual = send_res(method="get", url=gifts_list_url, headers=headers)
        send_res.close()
        return actual

    # 赠送礼物
    def send_gift(self, login_token, send_data):
        send_url = do_config("api", "url") + "gifts/send2"
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        # send_data = {"gift_id": 115, "receiver_id": 12707, "apply_content": "mmmm",
        #              "flag_apply": 0, "num": 1, "private_flag": 0}
        # 创建会话
        send_res = HandleRequest()
        actual = send_res(method="post", url=send_url, headers=headers, data=send_data, is_json=True)
        send_res.close()
        print(actual.json())
        return actual

    # 获取礼物赠送的id
    def get_record_id(self, login_token, send_data):
        actual = self.send_gift(login_token, send_data)
        return actual.json()["gift_record_id"]

    # 领取礼物
    def receive_gift(self, token, record_id):

        send_url = do_config("api", "url") + "gifts/record/" + record_id
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        # gift_id = do_config("gift", "gift_id")
        # 创建会话
        send_res = HandleRequest()
        actual = send_res(method="put", url=send_url, headers=headers, is_json=True)
        send_res.close()
        return actual

    # 获取礼物id的价值
    def get_gift_value(self, login_token, gift_id):
        gift_actual = self.get_gift_list(login_token)
        gift_list = gift_actual.json()["list"]
        for gift_value in gift_list:
            if gift_value["id"] == gift_id:
                return gift_value["value"]

        print("gift_id{}礼物不存在".format(gift_id))

    # 获取礼物id的价值
    def get_gift_id(self, login_token):
        gift_actual = self.get_gift_list(login_token)
        gift_list = gift_actual.json()["list"]
        gift_id_list = []
        for var in gift_list:
            gift_id_list.append(var["id"])

        gift_id = random.choice(gift_id_list)
        return gift_id

    # # 获取用户的好友请求列表
    # def friends_apply_list(self, token):
    #     url = do_config("api", "url") + "friends/apply?pos=0&limit=10&status=0"
    #     headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
    #                "app-version": "2.47.0"}
    #     send_res = HandleRequest()
    #     actual = send_res(method="get", url=url, headers=headers)
    #     send_res.close()
    #     return actual

    # 获取用户的好友请求列表
    def friends_apply_list(self, token):
        url = do_config("api", "url") + "chat/message?pos=0&limit=10&flag_type=3"
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
                   "app-version": "2.47.0"}
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers)
        send_res.close()
        return actual

    # 遍历获取第一个好友请求列表的请求id
    def friend_first_apply(self, token):
        actual = self.friends_apply_list(token)
        apply_list = actual.json()["list"]
        for i in apply_list:
            first_apply = i["id"]
            return first_apply

    # 接受好友请求
    def friends_apply(self, token, apply_id):
        url = do_config("api", "url") + "friends/apply"
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
                   "app-version": "2.47.0"}
        # apply_id = str(apply_id)
        data = {"id": apply_id, "result": "1"}
        send_res = HandleRequest()
        actual = send_res(method="put", url=url, data=data, headers=headers, is_json=True)
        send_res.close()
        return actual

    # 判断两人是不是好友
    def friend_relationship(self, token, user_id):
        pass


if __name__ == '__main__':
    obj = FriendBase()
    # login_actual = LoginBase().login(do_config("username", "A"))
    # print(login_actual.json())
    # login_token = login_actual.json()["token"]
    login_token = "46eeab6c6bd162f16cd35c35e038edf9"
    # actual = obj.get_user_friends(login_token)
    # print(actual.json())

    # send_data = {"gift_id": 303, "receiver_id": 18437, "apply_content": "mmmm",
    #              "flag_apply": 1, "num": 1, "private_flag": 0, "source": 1}
    #
    # obj.send_gift(login_token, send_data)

    actual = obj.friends_apply_list(login_token)
    print(actual.json())
    # first_apply = obj.friend_first_apply(login_token)
    # print(first_apply)

    # token = "68e826145212b5c36e182f9b247335c5"
    # for var in range(200):
    #     first_apply = obj.friend_first_apply(login_token)
    #     friends_apply_actual = obj.friends_apply(login_token, first_apply)
    #     print(friends_apply_actual.json())
