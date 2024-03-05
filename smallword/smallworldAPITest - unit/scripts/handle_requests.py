# -*- coding:utf-8 -*-
# @time     :2019/5/2822:25
# @Author   :xiaowang

import json
import requests
from scripts.constants import TEST_DATAS_FILE_PATH, CONFIG_USER_FILE_PATH, CONFIG_FILE_PATH
from scripts.handle_config import HandleConfig
from scripts.handle_pymusql import HandleMysql

# from scripts.handle_log import do_log


class HandleRequest:
    """
    封装一个请求的类。对应各种请求，进行处理。
    """
    def __init__(self):
        self.one_session = requests.Session()   # 创建一个session会话，记录cookies。

    def __call__(self, method, url, headers, data=None, files=None, is_json=False, **kwargs):
        method = method.lower()

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                # do_log.error("将json转换为python时，出现异常：{}".format(e))
                data = eval(data)

        if method == "get":
            res = self.one_session.request(method=method, url=url, params=data, headers=headers, **kwargs)
        elif method == "post":
            if files is None:
                if is_json:     # 判断是否时json，
                    res = self.one_session.request(method=method, url=url, json=data, headers=headers, **kwargs)
                else:
                    res = self.one_session.request(method=method, url=url, data=data, headers=headers, **kwargs)
            else:
                if is_json:     # 判断是否时json，
                    res = self.one_session.request(method=method, url=url, json=data, files=files, headers=headers, **kwargs)
                else:
                    res = self.one_session.request(method=method, url=url, data=data, files=files, headers=headers, **kwargs)
        elif method == "put":
            if is_json:     # 判断是否时json，
                res = self.one_session.request(method=method, url=url, json=data, headers=headers, **kwargs)
            else:
                res = self.one_session.request(method=method, url=url, data=data, headers=headers, **kwargs)
        elif method == "delete":
            res = self.one_session.request(method=method, url=url, params=data, headers=headers, **kwargs)
        else:
            res = None
            # do_log.error("不支持{}请求方法".format(method))

        return res

    def close(self):
        """
        关闭会话
        :return:
        """
        self.one_session.close()


if __name__ == '__main__':
    send_res = HandleRequest()
    # send_res()
    # de_config = HandleConfig(CONFIG_USER_FILE_PATH)
    # # url1 = "http://test.lemonban.com:8080/futureloan/mvc/api/member/register"
    # # url2 = "http://test.lemonban.com:8080/futureloan/mvc/api/member/login"
    # # url3 = "http://test.lemonban.com:8080/futureloan/mvc/api/member/recharge"
    # #
    # # params = {"mobilephone": "18711112222", "pwd": "123456", "regname": "WANG"}
    # # login_params = {"mobilephone": "18711112222", "pwd": "123456"}
    # # recharge_params = {"mobilephone": "18711112222", "amount": "2222"}
    # # headers = {"user-agent": "Mozilla/5.5 WANG/1.0.0"}
    # #
    # # # res1 = send_res("get", url1, params)
    # # # print(res1.json())  # 使用json格式显示
    # # # print(res1.text)  # 使用原始数据显示
    # # res2 = send_res("Post", url2, login_params)
    # # print(res2.json())  # 使用json格式显示
    # # print(res2.text)  # 使用原始数据显示
    # # res3 = send_res("PosT", url3, recharge_params)
    # # print(res3.json()["data"]["leaveamount"])  # 使用json格式显示
    # # print(res3.text)  # 使用原始数据显示
    # mobilephone = de_config("invest_user", "mobilephone")
    # print(mobilephone)
    # sql_amount = HandleMysql().is_existed_mobile_amount(mobilephone)
    # print(sql_amount)
    # send_res.close()

    str1 = '{"status": 0, "code": "20118", "data": null, "msg": "请输入数字"}'
    print(json.loads(str1))
    print(json.loads(str1)["data"])





