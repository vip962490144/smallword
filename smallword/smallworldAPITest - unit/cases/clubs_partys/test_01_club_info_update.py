    # -*- coding:utf-8 -*-
# @Author:Jaden.wang
import json
import time
import unittest

from libs.ddt import data, ddt
from scripts.constants import TEST_DATAS_FILE_PATH
from scripts.friend_and_chat.friend_base import FriendBase
from scripts.handle_excel import HandleExcel
from scripts.handle_log import do_log
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config

do_excel = HandleExcel(TEST_DATAS_FILE_PATH, "clubsinfo")


@ddt
class ClubsInfo(unittest.TestCase):
    """
    俱乐部信息更新
    """
    case_list = do_excel.get_cases()

    @classmethod
    def setUpClass(cls):
        """
        所有测试类执行之前执行此程序。
        :return:
        """
        cls.send_res = HandleRequest()
        do_log.info("\n{:*^40s}".format("开始执行俱乐部信息功能用例"))

        headers = {'content-type': 'application/json', 'authorization': 'Bearer '}  # +token#需要的话 传输token 用来用户权限验证
        login_url = do_config("api", "url") + "users/login"
        data = {"mobile": "17621620738", "password": "123456", "device": "android", "language": "ch", "area_code": "+86",
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
        do_log.info("\n{:*^40s}".format("俱乐部信息功能用例执行结束"))

    @data(*case_list)
    def test_case_01(self, data_ceses):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + self.token}
        case_id = data_ceses.case_id
        msg = data_ceses.title
        case_data = data_ceses.data
        case_url = do_config("api", "url") + data_ceses.url

        actual = self.send_res(method="put",
                               url=case_url,
                               data=case_data,
                               headers=headers,
                               is_json=True
                               )
        run_success_msg = do_config("msg", "success_result")
        run_fail_msg = do_config("msg", "fail_result")
        try:
            # data_ceses.expected = json.loads(data_ceses.expected)
            # data_ceses.expected = json.dumps(data_ceses.expected)
            actual_result = actual.json()
            # actual = json.loads(actual)
            # print(actual, type(actual))
            self.assertIn(data_ceses.expected, actual_result.values(),  msg="测试{}失败".format(msg))
        except AssertionError as e:
            do_log.error("具体异常为：{}".format(e))
            do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_fail_msg)
            raise e
        except KeyError as e:
            do_log.error("具体异常为：{}".format(e))
            do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_fail_msg)
            raise e
        else:
            do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_success_msg)


if __name__ == '__main__':
    unittest.main()


