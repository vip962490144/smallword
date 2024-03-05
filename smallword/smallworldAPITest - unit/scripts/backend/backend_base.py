# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import json

from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase


class BackendBase:
    # 后台操作类

    # 后台修改个人资料
    def updata_userinfo(self, login_token, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token,
                   'authorization-2': 'Bearer ' + login_token}
        end_url = do_config("api", "url") + "backend/users/info"
        # data_list = {"user_id": 12703, "diamond": "10000"}
        send_res = HandleRequest()
        actual = send_res(method="put", url=end_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 后台修改个人资料
    def send_diamond(self, login_token, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token,
                   'authorization-2': 'Bearer ' + login_token}
        end_url = do_config("api", "url") + "backend/users/diamond"
        # data_list = {"user_id": 12703, "diamond": "10000"}
        send_res = HandleRequest()
        actual = send_res(method="put", url=end_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 后台审核聚会
    def check_party(self, login_token, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        end_url = do_config("api", "url") + "backend/party/check"
        """
        |party_id|YES|聚会id|
        |result|Yes|审核结果 1 通过；-1 拒绝|
        |reason|No|拒绝理由|
        |modify_id|No|修改id，审核status为2时必传|
        """
        # data_list = {"party_id":7444,"result":1}
        send_res = HandleRequest()
        actual = send_res(method="post", url=end_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 获取后台邀请码列表
    def backend_invitation_code(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        end_url = do_config("api", "url") + "backend/statistic/invitation_code?" \
                                            "start=2020-1-11&stop=2020-1-20"
        send_res = HandleRequest()
        actual = send_res(method="get", url=end_url, headers=headers, is_json=True)
        send_res.close()
        return actual

    # 后台生成邀请码id
    def insert_invitation_code(self, token):

        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        end_url = do_config("api", "url") + "backend/statistic/insert_invitation_code"
        data = {"remarks": "自动注册", "grade": "4", 'number': '1'}

        send_res = HandleRequest()
        actual = send_res(method="post", url=end_url, headers=headers, data=data, is_json=True)
        send_res.close()
        return actual

    # 审核
    # 获取修改个人资料页面的审核信息，limit代表条数
    def get_updata_userinfo(self, login_token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        end_url = do_config("api", "url") + "backend/check?limit=20&type=modify"
        # data_list = {"user_id": 12703, "diamond": "10000"}
        send_res = HandleRequest()
        actual = send_res(method="get", url=end_url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 获取用户编辑列表的task_id
    def get_task_id(self, login_token, user_id):
        actual = self.get_updata_userinfo(login_token)
        actual_list = actual.json()["list"]
        task_id_list = []
        for var in actual_list:
            if var["user_id"] == user_id:
                task_id_list.append(var["id"])

        return task_id_list

    # 审核通过个人资料页面的审核信息
    def put_updata_userinfo(self, login_token, task_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        end_url = do_config("api", "url") + "backend/check"
        # data_list = {"user_id": 12703, "diamond": "10000"}
        data = {"task_id": task_id, "check_result": "approve"}
        send_res = HandleRequest()
        actual = send_res(method="put", url=end_url, data=data, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 传多个task时，同时审核通过
    def update_userinfo_more(self, login_token, task_id):
        task_id_list = task_id
        for task_id in task_id_list:
            actual = self.put_updata_userinfo(login_token, task_id)
            return actual

    # 后台设置黑卡会员
    def system_send_card(self, token, user_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
                   "authorization-2": 'Bearer ' + token}
        url = do_config("api", "backend_url") + "backend/users/system_send_card"
        # data_list = {"user_id": 12703, "diamond": "10000"}
        data = {"user_id": user_id, "card": 3}
        send_res = HandleRequest()
        actual = send_res(method="post", url=url, data=data, headers=headers, is_json=True)
        send_res.close()
        return actual

    # 写真集资格审核列表
    def get_photo_album_apply(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        # url = do_config("api", "url") + "backend/photo_album/apply?" \
        #                                 "pos=0&limit=100&mobile=17621620738" \
        #                                 "&area_code=+86&type=0"
        url = do_config("api", "url") + "backend/photo_album/apply?type=0"
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 写真集内容审核列表
    def get_photo_album(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        # url = do_config("api", "url") + "/backend/photo_album?" \
        #                                 "pos={pos}&limit={limit}&mobile={mobile}" \
        #                                 "&area_code={area_code}&type={type}&flag_sort={flag_sort}"
        url = do_config("api", "url") + "backend/photo_album?type=0"
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 写真集设置审核列表
    def get_photo_album_config(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "backend/photo_album/check_user_config?" \
                                        "pos={pos}&limit={limit}&mobile={mobile}" \
                                        "&area_code={area_code}&type={type}"
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 更改资格审核状态
    def put_photo_album_check_apply(self, token, apply_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "backend/photo_album/check_apply"
        data = {"id_arr": apply_id, "status": "1"}
        send_res = HandleRequest()
        actual = send_res(method="put", url=url, data=data, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 修改资格审核
    def put_photo_album_apply(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "backend/photo_album/apply"
        data = {"apply_id": 1, "context": "2"}
        send_res = HandleRequest()
        actual = send_res(method="put", url=url, data=data, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 更改审核内容状态
    def put_photo_album(self, token, apply_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "backend/photo_album/check_status"
        data = {"id_arr": apply_id, "status": "3"}
        send_res = HandleRequest()
        actual = send_res(method="put", url=url, data=data, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 更改设置审核状态
    def put_photo_album_config(self, token, apply_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "backend/photo_album/user_config_status"
        data = {"id_arr": [apply_id], "status": "2"}
        send_res = HandleRequest()
        actual = send_res(method="put", url=url, data=data, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 获取主题列表
    def get_photo_album_topics(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "backend/photo_album/topics?pos={pos}&limit={limit}"
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 新增主题
    def photo_album_topics(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "backend/photo_album/topics"
        data_list = {"title_arr": [1], "sort": "1"}
        send_res = HandleRequest()
        actual = send_res(method="POST", url=url, headers=headers, data=data_list, is_json=True)
        send_res.close()

        return actual

    # 遍历查询资格审核列表，获取id
    def get_user_photo_album_id(self, token, user_id):
        actual = self.get_photo_album_apply(token)
        apply_list = actual.json()["list"]
        apply_list_id = []
        for var in apply_list:
            apply_user_id = var["user"]["id"]
            if user_id == apply_user_id:
                apply_list_id.append(var["apply_id"])

        return apply_list_id

    # 遍历查询内容审核列表，获取所有自己的内容列表id
    def get_user_photo_album_list_id(self, token, user_id):
        actual = self.get_photo_album(token)
        list_photo_album = actual.json()["list"]
        list_id = []
        for var in list_photo_album:
            apply_id = var["user"]["id"]
            if user_id == apply_id:
                list_id.append(var["id"])

        return list_id

    # 关闭聚会
    def backend_party_close(self, token, id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "backend/party/info/{}".format(id)
        # data_list = {"title_arr": [1], "sort": "1"}
        send_res = HandleRequest()
        actual = send_res(method="DELETE", url=url, headers=headers, is_json=True)
        send_res.close()

        return actual


if __name__ == '__main__':
    obj = BackendBase()
    A = '{"mobile": "17621620970", "password": "123456"}'
    login_actual = LoginBase().login(A)
    user_id = login_actual.json()["user_info"]["id"]
    print(user_id)
    login_token = LoginBase().get_backend_token(do_config("admin", "C"))
    print(login_token)

    actual = obj.get_updata_userinfo(login_token)
    print(actual.json())
    task_id_list = obj.get_task_id(login_token, user_id)
    print(task_id_list)
    actual = obj.update_userinfo_more(login_token, task_id_list)
    print(actual)
    # for task_id in task_id_list:
    #     actual = obj.put_updata_userinfo(login_token, task_id)
    #     print(actual.text)
