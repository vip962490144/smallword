# -*- coding:utf-8 -*-
# @time     :2019/5/2821:56
# @Author   :xiaowang
# @File     :lemon_requests_0527.py

from libs.ddt import ddt, data
import unittest
# import inspect
from scripts.Base import Base
from scripts.constants import TEST_USER_DATAS_USER3_FILE_PATH, TEST_DATAS_FILE_PATH
from scripts.handle_excel import HandleExcel
from scripts.handle_log import do_log
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config


@ddt
class HandleLogin(unittest.TestCase):
    """
    测试用例类
    """
    # case_list = do_excel.get_cases()
    # case_list = [{"mobile": "17621620738", "password": "a123456"}, {"mobile": "17621620738", "password": "a1234567"}]
    case_list = Base().read_user(TEST_USER_DATAS_USER3_FILE_PATH)

    @classmethod
    def setUpClass(cls):
        """
        所有测试类执行之前执行此程序。
        :return:
        """
        cls.send_res = HandleRequest()
        do_log.info("\n{:*^40s}".format("开始执行登录功能用例"))

    @classmethod
    def tearDownClass(cls):
        """
        所有测试类执行之后执行此程序。
        :return:
        """
        cls.send_res.close()
        do_log.info("\n{:*^40s}".format("登录功能用例执行结束"))

    # @data(*case_list)
    # def test_case_01(self, data_ceses):
    #     do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
    #     case_id = data_ceses.case_id
    #     msg = data_ceses.title
    #     case_data = HandleContext().register_parameterization(data_ceses.data)
    #     case_url = do_config("api", "url") + data_ceses.url
    #     actual = self.send_res(method=data_ceses.method,
    #                            url=case_url,
    #                            data=case_data)
    #     run_success_msg = do_config("msg", "success_result")
    #     run_fail_msg = do_config("msg", "fail_result")
    #     try:
    #         self.assertEqual(data_ceses.expected, actual.text, msg="测试{}失败".format(msg))
    #     except AssertionError as e:
    #         do_log.error("具体异常为：{}".format(e))
    #         do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_fail_msg)
    #         raise e
    #     else:
    #         do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_success_msg)

    @data(*case_list)
    def test_case_01(self, data_cases):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer '}  # +token#需要的话 传输token 用来用户权限验证
        login_url = do_config("api", "url") + "users/login"

        mobile = data_cases["mobile"]
        password = data_cases["password"]

        data = {"mobile": mobile, "password": password, "device": "android", "language": "ch", "area_code": "+86",
                "device_no": "test", "phone_type": "9500", "system": "28", "idfa": "test"}

        actual = self.send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
        msg = "测试正常登录"

        try:
            login_token = actual.json()["token"]
            self.assertNotEqual("", login_token, msg="测试{}失败".format(msg))
        except AssertionError as e:
            do_log.error("具体异常为：{}".format(e))
            raise e
        except KeyError as e:
            do_log.error("具体异常为：{}".format(e))
            raise e
        else:
            print("测试通过")
            # print(actual.json())


if __name__ == '__main__':
    unittest.main()
