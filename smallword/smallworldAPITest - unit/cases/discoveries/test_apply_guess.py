# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import json
import time
import unittest

from libs.ddt import ddt,data
from scripts.Base import Base
from scripts.activities_and_discoveries.discover_base import DiscoverBase
from scripts.backend.backend_base import BackendBase
from scripts.constants import TEST_ONE_DATAS_USER_FILE_PATH
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config, HandleConfig
from scripts.logins.login_base import LoginBase


@ddt
class ApplyGuess(unittest.TestCase):
    """
    用户竞猜
    """

    data_list = Base().read_user(TEST_ONE_DATAS_USER_FILE_PATH)


    # @classmethod
    # def setUpClass(cls):
    #     """
    #     所有测试类执行之前执行此程序。
    #     :return:
    #     """
    #     cls.send_res = HandleRequest()
    #
    # def tearDownClass(cls):
    #     """
    #     所有测试类执行之后执行此程序。
    #     :return:
    #     """
    #     cls.send_res.close()

    @data(*data_list)
    def test_case_01(self, data_list):
        # print(data_list)
        data_list = json.dumps(data_list)
        data_list = json.loads(data_list)
        # print(type(data_list))
        # data_list = json.loads(data_list)
        mobile = data_list["mobile"]
        # print(mobile)
        data_list = json.dumps(data_list)
        a_login_actual = LoginBase().login(data_list)
        # print(a_login_actual.json())
        a_login_id = a_login_actual.json()["user_info"]["id"]
        # 后台登录，使用用户id，修改用户数据，充值10000
        login_actual = LoginBase().backend_login(do_config("admin", "A"))
        # print(login_actual.json())
        login_token = login_actual.json()["token"]
        backend_data_list = {"user_id": a_login_id, "diamond": "10000"}
        user_update_actual = BackendBase().updata_userinfo(login_token, backend_data_list)

        # 登录app，进行竞猜
        a_login_actual = LoginBase().login(data_list)
        a_login_token = a_login_actual.json()["token"]
        # print(a_login_actual.json())
        data_list = Base().random_num(10)
        guess_actual = DiscoverBase().random_guess(a_login_token, data_list)

        # print(user_update_actual.json())
        print(guess_actual.text)


if __name__ == '__main__':
    unittest.main()
