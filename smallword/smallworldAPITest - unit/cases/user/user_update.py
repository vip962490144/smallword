# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import json
import time
import unittest

from libs.ddt import ddt,data
from scripts.Base import Base
from scripts.backend.backend_base import BackendBase
from scripts.constants import TEST_ONE_DATAS_USER_FILE_PATH, TEST_TWO_DATAS_USER_FILE_PATH, \
    TEST_USER_DATAS_USER_FILE_PATH
from scripts.handle_config import do_config
from scripts.logins.login_base import LoginBase


@ddt
class UserUpdate(unittest.TestCase):
    """
    用户资料更新
    """
    login_one_data_list = Base().read_user(TEST_USER_DATAS_USER_FILE_PATH)
    login_two_data_list = Base().read_user(TEST_TWO_DATAS_USER_FILE_PATH)

    @data(*login_one_data_list)
    def test_case_01(self, data_list):
        data_list = json.dumps(data_list)
        a_login_actual = LoginBase().login(data_list)
        a_login_id = a_login_actual.json()["user_info"]["id"]
        # 后台登录，使用用户id，修改用户数据，充值1000000
        login_actual = LoginBase().backend_login(do_config("admin", "A"))
        login_token = login_actual.json()["token"]
        backend_data_list = {"user_id": a_login_id, "diamond": "1000000"}
        user_update_actual = BackendBase().updata_userinfo(login_token, backend_data_list)

    @data(*login_two_data_list)
    def test_case_02(self, data_list):
        data_list = json.dumps(data_list)
        a_login_actual = LoginBase().login(data_list)
        a_login_id = a_login_actual.json()["user_info"]["id"]
        # 后台登录，使用用户id，修改用户数据，充值1000000
        login_actual = LoginBase().backend_login(do_config("admin", "A"))
        login_token = login_actual.json()["token"]
        backend_data_list = {"user_id": a_login_id, "diamond": "1000000"}
        user_update_actual = BackendBase().updata_userinfo(login_token, backend_data_list)


if __name__ == '__main__':
    unittest.main()

