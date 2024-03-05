# -*- coding:utf-8 -*-
# @Author:Jaden.wang
import json
import time
import unittest

from libs.ddt import data, ddt
from scripts.activities_and_discoveries.file_base import FileBase
from scripts.constants import TEST_DATAS_FILE_PATH
from scripts.friend_and_chat.friend_base import FriendBase
from scripts.handle_context import HandleContext
from scripts.handle_excel import HandleExcel
from scripts.handle_log import do_log
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config
from scripts.upload.ufile.postfile import postfile

do_excel = HandleExcel(TEST_DATAS_FILE_PATH, "file")


@ddt
class GetTheWall(unittest.TestCase):
    """
    发布世界墙，断言
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
        do_log.info("\n{:*^40s}".format("赠送礼物功能用例执行结束"))

    @data(*case_list)
    def test_case_01(self, data_ceses):
        login_token = self.token
        # headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + self.token}
        case_id = data_ceses.case_id
        msg = data_ceses.title
        localfile = data_ceses.data
        data = FileBase().get_file_type(localfile)

        # 判断创建世界墙是否需要钻石
        FileBase().get_the_wall_diamond(login_token)

        # 创建世界墙
        actual = FileBase().creat_the_wall(login_token, self.user_id)
        moment_id = actual.json()["id"]

        # 创建文件上传
        actual = FileBase().create_post_file(login_token, data)
        file_id = actual.json()["file_id"]
        signature = actual.json()["signature"]
        file_url = actual.json()["file_url"]
        # 上传文件到ucloud
        postfile(file_url, signature, file_id, localfile)
        actual = FileBase().put_file_end(login_token, file_id, moment_id)
        print(actual)

        run_success_msg = do_config("msg", "success_result")
        run_fail_msg = do_config("msg", "fail_result")
        # if data_ceses.expected is None:
        #     try:
        #         gift_record_id = actual.json()["gift_record_id"]
        #         if gift_record_id:
        #             HandleContext.record_id = gift_record_id
        #         self.assertIsNotNone(gift_record_id, msg="测试{}失败".format(msg))
        #     except AssertionError as e:
        #         do_log.error("具体异常为：{}".format(e))
        #         do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_fail_msg)
        #         raise e
        #     except KeyError as e:
        #         do_log.error("具体异常为：{}".format(e))
        #         do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_fail_msg)
        #         raise e
        #     else:
        #         do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_success_msg)
        # else:
        #     try:
        #         error_message = actual.json()["error_message"]
        #         expected = json.loads(data_ceses.expected)["error_message"]
        #         self.assertEqual(expected, error_message, msg="测试{}失败".format(msg))
        #     except AssertionError as e:
        #         do_log.error("具体异常为：{}".format(e))
        #         do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_fail_msg)
        #         raise e
        #     except KeyError as e:
        #         do_log.error("具体异常为：{}".format(e))
        #         do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_fail_msg)
        #         raise e
        #     else:
        #         do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_success_msg)


if __name__ == '__main__':
    unittest.main()


