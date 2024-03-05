# -*- coding:utf-8 -*-
# @Author:Jaden.wang
import time
import unittest

from libs.ddt import data, ddt
from scripts.constants import TEST_DATAS_FILE_PATH
from scripts.friend_and_chat.friend_base import FriendBase
from scripts.handle_excel import HandleExcel
from scripts.handle_context import HandleContext
from scripts.handle_log import do_log
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config
from scripts.others.others_base import OthersBase

do_excel = HandleExcel(TEST_DATAS_FILE_PATH, "recive_gift")


@ddt
class ReciveGift(unittest.TestCase):
    """
    收礼物,断言
    """
    case_list = do_excel.get_cases()

    @classmethod
    def setUpClass(cls):
        """
        所有测试类执行之前执行此程序。
        :return:
        """
        cls.send_res = HandleRequest()
        do_log.info("\n{:*^40s}".format("开始执行赠送礼物功能用例"))

        headers = {'content-type': 'application/json', 'authorization': 'Bearer '}  # +token#需要的话 传输token 用来用户权限验证
        login_url = do_config("api", "url") + "users/login"
        data = {"mobile": "17621620737", "password": "a123456", "device": "android", "language": "ch", "area_code": "+86",
                "device_no": "test", "phone_type": "9500", "system": "28", "idfa": "test"}
        actual = cls.send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
        cls.token = actual.json()["token"]
        cls.user_id = actual.json()["user_info"]["id"]

    @classmethod
    def tearDownClass(cls):
        """
        所有测试类执行之后执行此程序。
        :return:
        """
        cls.send_res.close()
        do_log.info("\n{:*^40s}".format("开始执行赠送礼物功能用例"))

    @data(*case_list)
    def test_case_01(self, data_ceses):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + self.token}

        case_id = data_ceses.case_id
        msg = data_ceses.title
        method = data_ceses.method
        send_url = do_config("api", "url") + data_ceses.url

        case_url = HandleContext.record_id_replace(send_url)
        run_success_msg = do_config("msg", "success_result")
        run_fail_msg = do_config("msg", "fail_result")

        if data_ceses.method == "put":
            actual = self.send_res(method=method,
                                   url=case_url,
                                   headers=headers,
                                   is_json=True
                                   )
            try:
                self.total_ticket = actual.json()["total_ticket"]
                self.assertIsNotNone(actual.json()["gift"], msg="测试{}失败".format(msg))
            except AssertionError as e:
                do_log.error("具体异常为：{}".format(e))
                do_excel.write_result(row=case_id + 1, actual=e, result=run_fail_msg)
                raise e
            except KeyError as e:
                do_log.error("具体异常为：{}".format(e))
                do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_fail_msg)
                raise e
            else:
                do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_success_msg)
        else:
            if data_ceses.expected is None:
                actual = self.send_res(method=method,
                                       url=case_url,
                                       headers=headers,
                                       is_json=True
                                       )
                ranking_list = actual.json()["list"]
                user_amount = 0
                for var in ranking_list:
                    if int(self.user_id) == int(var["user_id"]):
                        user_amount = var["amount"]
                        break
                    user_amount = "user_id,{}此用户不在榜单中".format(self.user_id)

                try:
                    if user_amount:
                        HandleContext.user_amount = user_amount
                    self.assertIsNotNone(user_amount, msg="测试{}失败".format(msg))
                except AssertionError as e:
                    do_log.error("具体异常为：{}".format(e))
                    do_excel.write_result(row=case_id + 1, actual=e, result=run_fail_msg)
                    raise e
                else:
                    do_excel.write_result(row=case_id + 1, actual=user_amount, result=run_success_msg)
            else:
                actual = self.send_res(method=method,
                                       url=case_url,
                                       headers=headers,
                                       is_json=True
                                       )
                ranking_list = actual.json()["list"]
                berfore_user_amount = HandleContext.user_amount_replace(data_ceses.expected)
                user_amount = 0
                for var in ranking_list:
                    if int(self.user_id) == int(var["user_id"]):
                        user_amount = var["amount"]
                        break
                    user_amount = "user_id,{}此用户不在榜单中".format(self.user_id)

                try:
                    # self.assertEqual(data_ceses.expected, actual.text, msg="测试{}失败".format(msg))
                    list_difference = [1, 0]
                    user_amount_difference = int(user_amount) - int(self.total_ticket) - int(berfore_user_amount)
                    self.assertIn(user_amount_difference, list_difference, msg="测试{}失败".format(msg))
                except AssertionError as e:
                    do_log.error("具体异常为：{}".format(e))
                    do_excel.write_result(row=case_id + 1, actual=1, result=run_fail_msg)
                    raise e
                else:
                    do_excel.write_result(row=case_id + 1, actual=user_amount_difference, result=run_success_msg)


if __name__ == '__main__':
    unittest.main()


