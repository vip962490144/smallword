# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import random
import time

from selenium import webdriver
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase


class RedpacketBase:
    # 红包操作类

    # 获取发送红包信息
    def send_redpacket(self, login_token, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        club_redpacket_url = do_config("api", "url") + "clubs/packet"
        # data_list = {"club_id":"1846","user_num":"3","total_money":"102","memo":"美女才可以领"}
        send_res = HandleRequest()
        actual = send_res(method="post", url=club_redpacket_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 俱乐部冒险游戏红包
    def club_adventure_game(self, token, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        club_redpacket_url = do_config("api", "url") + "club_adventure_game"
        # data_list = {"club_id": "1846", "type": 1, "user_num": "3", "punish_num": "2",
        #              "total_money": "100", "adventure_conetent": "美女才可以领"}
        send_res = HandleRequest()
        actual = send_res(method="post", url=club_redpacket_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 获取红包id
    def get_redpacket_id(self, login_token, data_list):
        redpacket_actual = self.send_redpacket(login_token, data_list)
        redpacket_id = redpacket_actual.json()["id"]

        return redpacket_id

    # 领取红包
    def receive_redpacket(self, login_token, redpacket_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        club_redpacket_url = do_config("api", "url") + "clubs/packet/" + redpacket_id
        send_res = HandleRequest()
        actual = send_res(method="put", url=club_redpacket_url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 获取问卷题目
    def get_question(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        get_question_url = do_config("api", "url") + "question/choice?language=0"
        res = HandleRequest()
        actual = res(method="get", url=get_question_url, headers=headers)
        res.close()
        return actual

    # 获取问卷id和答案id
    def get_question_id(self, token):
        actual = self.get_question(token)
        subject_id = actual.json()["subject"]["subject_id"]
        answer = actual.json()["subject"]["answer"]
        answer_list = []
        for i in range(len(answer)):
            var = answer[i]["id"]
            answer_list.append(var)
        return subject_id, answer_list

    # 填写问卷
    def do_question(self, token, subject_id, answer_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        do_question_url = do_config("api", "url") + "question/dochoice"
        data = {"subject_id": subject_id, "answer_id": answer_id}
        res = HandleRequest()
        actual = res(method="post", url=do_question_url, data=data, headers=headers, is_json=True)
        res.close()
        return actual

    # 发布问卷红包
    def question_release(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        question_release_url = do_config("api", "url") + "question/release"
        data = {"money": "1000"}
        res = HandleRequest()
        actual = res(method="post", url=question_release_url, data=data, headers=headers, is_json=True)
        res.close()
        return actual

    # 中断问卷填写发布
    def question_dumpchoice(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        question_dumpchoice_url = do_config("api", "url") + "question/dumpchoice"
        res = HandleRequest()
        actual = res(method="GET", url=question_dumpchoice_url, headers=headers)
        res.close()
        return actual

    # 获取世界问卷题目
    def get_question_joinanswer(self, token, questionnaire_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        question_joinanswer_url = do_config("api", "url") + \
                                  "question/joinanswer?questionnaire_id={}".format(questionnaire_id)
        res = HandleRequest()
        actual = res(method="GET", url=question_joinanswer_url, headers=headers)
        res.close()
        return actual

    # 填写世界问卷题目
    def question_joinanswer(self, token, questionnaire_id, choice_question_id, answer_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        question_joinanswer_url = do_config("api", "url") + \
                                  "question/joinanswer?questionnaire_id={}".format(questionnaire_id)
        data = {"choice_question_id": choice_question_id, "answer_id": answer_id}
        res = HandleRequest()
        actual = res(method="post", url=question_joinanswer_url, data=data, headers=headers, is_json=True)
        res.close()
        return actual

    # 每日红包脚本触发
    @staticmethod
    def everyday_redpacket():
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        url1 = "http://106.75.11.161:8082/backend/task/createpacket"
        url2 = "http://106.75.11.161:8082/backend/task/sendpacket"
        driver.get(url1)
        time.sleep(5)
        driver.get(url2)
        time.sleep(30)
        row = driver.find_element_by_xpath('//body')
        name = row.get_attribute('textContent')
        if name is not None:
            driver.close()
            return True
        else:
            return False

    # 聚会红包
    def send_party_packet(self, login_token, party_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        url = do_config("api", "url") + "party/packet"
        data = {"party_id": party_id}
        res = HandleRequest()
        actual = res(method="post", url=url, data=data, headers=headers, is_json=True)
        res.close()
        return actual

    # 创建礼物红包
    def create_raffle_gifts(self, token, sku_data, club_id=None):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "mallProduct/create_raffle_gifts"
        if club_id is None:
            data = {"note": "dolor",
                    "sku_data": sku_data
                    }
        else:
            data = {"note": "dolor", "club_id": club_id,
                    "sku_data": sku_data
                    }
        res = HandleRequest()
        actual = res(method="post", url=url, data=data, headers=headers, is_json=True)
        res.close()
        return actual

    # 获取礼物红包商品列表
    def get_raffle_gift_list(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "mallProduct/get_raffle_gift_list"
        res = HandleRequest()
        actual = res(method="get", url=url, headers=headers, is_json=True)
        res.close()
        return actual

    # 获取礼物红包的商品数组
    def get_sku_data(self, token):
        actual = self.get_raffle_gift_list(token)
        gift_list = actual.json()["list"]
        gift_id_list = []
        for var in gift_list:
            id = var["id"]
            gift_id_list.append(id)

        sku_data = []
        for var in gift_id_list:
            num = random.randint(1, 3)
            gift_id = var
            gift_info = {"gift_draw_spu_id": gift_id, "num": num}
            sku_data.append(gift_info)
        return sku_data

    # 领取红包进行抽奖
    def lucky_draw(self, token, gift_draw_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "mallProduct/initiate_lucky_draw"
        data = {"gift_draw_id": gift_draw_id}
        res = HandleRequest()
        actual = res(method="post", url=url, data=data, headers=headers, is_json=True)
        res.close()
        return actual

    # 礼物红包支付
    def pay_raffle_gift_order(self, token, gift_draw_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "charge/pay_raffle_gift_order"
        data = {"gift_draw_id": gift_draw_id}
        res = HandleRequest()
        actual = res(method="post", url=url, data=data, headers=headers, is_json=True)
        res.close()
        return actual

    # 烟花红包
    def send_firework(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        # url = "http://106.75.29.100:8081/" + "redPacket/send_firework"
        url = do_config("api", "url") + "redPacket/send_firework"
        data = {"num": 3}
        res = HandleRequest()
        actual = res(method="post", url=url, data=data, headers=headers, is_json=True)
        res.close()
        return actual

    # 获取红包倒计时
    def get_count_down_list(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        # url = "http://106.75.29.100:8081/" + "redPacket/count_down_list"
        url = do_config("api", "url") + "redPacket/count_down_list"

        res = HandleRequest()
        actual = res(method="get", url=url, headers=headers)
        res.close()
        return actual

    # 领取烟花红包
    def receive_firework(self, token, packet_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        # url = "http://106.75.29.100:8081/" + "redPacket/receive_firework"
        url = do_config("api", "url") + "redPacket/receive_firework"

        datalist = {"id": packet_id}
        res = HandleRequest()
        actual = res(method="post", url=url, data=datalist, headers=headers, is_json=True)
        res.close()
        return actual

    # 发送弹幕


if __name__ == '__main__':
    # login_actual = LoginBase().login(do_config("username", "A"))
    # login_actual = LoginBase().login(login_data)
    # a_token = login_actual.json()["token"]
    # print(login_actual.json())
    obj = RedpacketBase()
    # sku_data = obj.get_sku_data(a_token)
    # print(sku_data)
    # actual = obj.get_raffle_gift_list(login_token)
    # print(actual.json())
    # actual = obj.create_raffle_gifts(a_token, sku_data)
    # print(actual.json())
    # gift_draw_id = actual.json()["gift_draw_id"]
    # print(gift_draw_id)
    # actual = obj.pay_raffle_gift_order(a_token, gift_draw_id)
    # print(actual.json())
    login_actual = LoginBase().login(do_config("username", "A"))
    # print(login_actual.json())
    id = login_actual.json()["user_info"]["id"]
    # print(id)
    b_token = login_actual.json()["token"]
    # print(b_token)
    # actual = obj.lucky_draw(b_token, gift_draw_id)
    # print(actual.json())
    # list_num = [1, 2, 3, 4]
    for var in range(10):
        actual = obj.send_firework(b_token)
        print(actual.text)
    actual = obj.get_count_down_list(b_token)
    print(actual.json())
    end_time = actual.json()["countdown_list"][0]["end_time"]
    packet_id = actual.json()["countdown_list"][0]["packet_id"]
    print(end_time)
    # login_actual = LoginBase().login(do_config("username", "B"))
    # a_token = login_actual.json()["token"]
    # user_id = login_actual.json()["user_info"]["id"]
    # print(user_id)
    # time.sleep(30)
    # actual = obj.receive_firework(a_token, packet_id)
    # print(actual.text)



