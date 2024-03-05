# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import json
import os
import time
import unittest

from libs.ddt import ddt, data
from scripts.Base import Base
from scripts.backend.backend_base import BackendBase
from scripts.constants import TEST_ONE_DATAS_USER_FILE_PATH, TEST_TWO_DATAS_USER_FILE_PATH, CONFIGS_DIR, BASE_DIR
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config, HandleConfig
from scripts.logins.login_base import LoginBase
from scripts.user_info.user_base import UserBase


class UserPwd:
    """
    用户资料更新
    """

    def login(self, mobile):
        # 返回登录的token
        headers = {'content-type': 'application/json', 'authorization': 'Bearer '}
        login_url = do_config("api", "url") + "users/login"
        # mobile = data_list["mobile"]
        # password = data_list["password"]
        data = {"mobile": mobile, "password": "123456",
                "device": "android", "language": "ch",
                "area_code": "+86", "device_no": "test",
                "phone_type": "9500", "system": "28", "idfa": "test"}
        send_res = HandleRequest()
        actual = send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
        send_res.close()
        return actual

    # 忘记密码
    def updata_pwd(self, data):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer '}
        login_url = do_config("api", "url") + "users/password"

        send_res = HandleRequest()
        actual = send_res(method="put", url=login_url, headers=headers, data=data, is_json=True)
        send_res.close()
        return actual

    # 获取邀请码
    def get_code(self, token, code_id):
        invitation_code_actual = BackendBase().backend_invitation_code(token)
        list_actual = invitation_code_actual.json()["list"]
        for i in range(len(list_actual)):
            id = list_actual[i]["id"]
            if code_id == id:
                return list_actual[i]["invitation_code"]
        print("无此兑换码{}".format(code_id))

    # 邀请码登录，生成，返回邀请码
    def get_code_num(self):
        # 生成邀请码
        backend_login_token = LoginBase().get_backend_token(do_config("admin", "A"))
        # 生成获取邀请码id
        code_actual = BackendBase().insert_invitation_code(backend_login_token)
        time.sleep(1)
        code_id = code_actual.json()["id"]
        # 拿到邀请码
        code = self.get_code(backend_login_token, code_id)
        return code


if __name__ == '__main__':
    # A = {"mobile": "17621620898", "password": "123456"}
    obj = UserPwd()
    i = 17777149662  # 起始手机号
    for a in range(338):
        mobile = str(i)
        # actual = LoginBase().check_mobile(mobile)
        # check_id = actual.json()["is_check"]
        # 获取验证码
        res = LoginBase().captcha(mobile)
        # print(res.text)
        # 注册
        actual = LoginBase().register(mobile)
        # print(actual.text)
        # 登录
        # actual = obj.login(mobile)
        time.sleep(1)
        login_token = actual.json()["token"]
        user_id = actual.json()["user_info"]["id"]
        nicknum = Base().num_to_char(mobile[-4:])
        # 选性别
        data = {"gender": 0}
        users_info_actual = UserBase().choice_gender(login_token, data)
        # print(users_info_actual)
        # print(users_info_actual.json())
        time.sleep(1)
        # time.sleep(1)
        data = {"nickname": "NV" + nicknum}
        users_actual = UserBase().fill_nickname(login_token, data)
        # print(users_actual)
        # print(users_actual.text)
        time.sleep(1)
        # # 登录后台
        token = "4054923a21ba63edf553e6366272d86751159ced"
        # # 后台修改人气等级
        data_list = {"user_id": user_id, "rp_level": 3, "flag_rp_check": 2, "flag_send_world_notice": 0,
                     "flag_rp_vip_not_send_notice": 0}
        actual = BackendBase().updata_userinfo(token, data_list)
        # print(actual.json())
        # 后台充值 1000000
        data_list = {"diamond_change": "1000000", "flag_compensate": 0, "user_id": user_id}
        actual = BackendBase().send_diamond(token, data_list)
        # print(actual.json())
        # 写入文件
        time.sleep(1)
        Base().write_config(mobile)
        i += 1

    print("--end--")