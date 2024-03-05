# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import time

from scripts.activities_and_discoveries.discover_base import DiscoverBase
from scripts.backend.backend_base import BackendBase
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase
from scripts.redpackets.redpacket_base import RedpacketBase


class PartyBase:
    # 聚会操作类

    # 发布聚会
    def create_party(self, login_token, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        create_panty_url = do_config("api", "url") + "party"

        # data_list = {"name":"纯high聚会","appoint_time":1526610257,"city":"上海",
        #              "location":"漕宝路650号","location_uid":"11122311",
        #              "num":2,"packet_money":1000,"ticket_hotel_flag":1,
        #              "description":"赶快进来high","address":"上海徐汇区","type":1,
        #              "club_id":122,"flag_anonymous":1}

        send_res = HandleRequest()
        actual = send_res(method="post", url=create_panty_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 获取发布聚会id
    def get_party_id(self, login_token, data_list):
        actual = self.create_party(login_token, data_list)
        party_id = actual.json()["id"]

        return party_id

    # 获取我所有的聚会
    def get_all_party(self, login_token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        get_all_party_url = do_config("api", "url") + "party?limit=100&pos=0&type=2"

        send_res = HandleRequest()
        actual = send_res(method="get", url=get_all_party_url, headers=headers)
        send_res.close()

        return actual

    # 参加聚会
    def apply_for_party(self, login_token, party_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        apply_panty_url = do_config("api", "url") + "party/apply"
        data_list = {"party_id": party_id, "be_present_flag": 1, "airline_ticket_flag": 1,
                     "hotel_flag": 1, "remarks": "想参加"}
        send_res = HandleRequest()
        actual = send_res(method="post", url=apply_panty_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 同意他人加入聚会的申请
    def handle_apply(self, login_token, apply_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        apply_panty_url = do_config("api", "url") + "party/applications/{}".format(apply_id)
        send_res = HandleRequest()
        actual = send_res(method="put", url=apply_panty_url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 聚会签到
    def party_signup(self, token, party_id, lat, lon):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
                   "app-version": "2.9.15"}
        url = do_config("api", "url") + "/party/signup"
        data_list = {"party_id": party_id, "lat": lat, "lon": lon}
        send_res = HandleRequest()
        actual = send_res(method="POST", url=url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 修改聚会信息
    def update_party_info(self, token, data, party_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "party/{}".format(party_id)
        send_res = HandleRequest()
        actual = send_res(method="put", url=url, data=data, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 关闭聚会
    def close_party(self, login_token, id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        panty_url = do_config("api", "url") + "party/close_party/{}".format(id)
        send_res = HandleRequest()
        actual = send_res(method="DELETE", url=panty_url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 取消聚会
    def party_action(self, login_token, id, action=2):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        if action == "退出聚会":
            action = 1
        else:
            action = 2
        panty_url = do_config("api", "url") + "/party/{}?action={}".format(id, action)
        send_res = HandleRequest()
        actual = send_res(method="DELETE", url=panty_url, headers=headers, is_json=True)
        send_res.close()

        return actual


if __name__ == '__main__':
    time_num = int(time.time()) + 43200
    a_login_actual = LoginBase().login(do_config("username", "A"))
    a_login_token = a_login_actual.json()["token"]
    obj = PartyBase()
    # modular_id = DiscoverBase().get_modular_id(a_login_token)
    # merchant_id = DiscoverBase().get_merchant_id(a_login_token, modular_id)
    data_list = {"name": "纯high聚会", "appoint_time": time_num, "city": "上海",
                 "location": "漕宝路650号", "location_uid": "11122311",
                 "num": 2, "packet_money": 1000, "ticket_hotel_flag": 1,
                 "description": "赶快进来high", "address": "上海徐汇区", "type": 1,
                 "flag_anonymous": 0, "merchant_id": 1}

    party_id = obj.get_party_id(a_login_token, data_list)
    print(party_id)

    data_list1 = {"party_id": party_id, "result": 1}

    token = LoginBase().get_backend_token(do_config("admin", "A"))
    BackendBase().check_party(token, data_list1)
    login_actual = LoginBase().login(do_config("username", "B"))
    login_token = login_actual.json()["token"]
    actual = obj.apply_for_party(login_token, party_id)
    print(actual.json()["id"])
    apply_id = actual.json()["id"]

    a_login_actual = LoginBase().login(do_config("username", "A"))
    a_login_token = a_login_actual.json()["token"]
    actual = obj.handle_apply(a_login_token, apply_id)
    print(actual.json())

    data_list2 = {"appoint_time": 0}

    actual = obj.update_party_info(a_login_token, data_list2, party_id)
    print(actual.json())

    time.sleep(5)

    actual = RedpacketBase().send_party_packet(a_login_token, party_id)
    print(actual.json())

    redpacket_id = actual.json()["id"]

    actual = RedpacketBase().receive_redpacket(login_token, redpacket_id)
    print(actual.text)
