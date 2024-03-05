# -*- coding:utf-8 -*-
# @time     :2019/5/2821:56
# @Author   :xiaowang
# @File     :lemon_requests_0527.py
import random

from libs.ddt import ddt, data
import unittest
# import inspect
# from scripts.Base import Base
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config
# from scripts.handle_excel import HandleExcel
# from scripts.handle_log import do_log
# from scripts.constants import TEST_DATAS_FILE_PATH
# from scripts.handle_context import HandleContext

# do_excel = HandleExcel(TEST_DATAS_FILE_PATH, "login")
from scripts.logins.login_base import LoginBase


class SubmitTask(unittest.TestCase):
    """
    测试用例类
    """
    @classmethod
    def setUpClass(cls):
        """
        所有测试类执行之前执行此程序。
        :return:
        """
        cls.send_res = HandleRequest()
        # do_log.info("\n{:*^40s}".format("开始执行登录功能用例"))

    @classmethod
    def tearDownClass(cls):
        """
        所有测试类执行之后执行此程序。
        :return:
        """
        cls.send_res.close()

    def test_case_01(self):
        login_actual = LoginBase().login(do_config("username", "A"))
        login_token = login_actual.json()["token"]
        headers = {'content-type':'application/json', 'authorization': 'Bearer ' + login_token}  # +token#需要的话 传输token 用来用户权限验证
        submit_url = do_config("api", "url") + "competition/like"

        # competition_id = random.rand(1261, 1262, 1263)

        data_list = {"submit_id": 1261,'like_num': 22}

        actual = self.send_res(method="post", url=submit_url, headers=headers, data=data_list, is_json=True)

        print(actual)


if __name__ == '__main__':
    unittest.main()



