# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import json
import random
import time
import unittest

# from scripts.Base import Base
from libs.ddt import ddt, data
from scripts.Base import Base
from scripts.constants import TEST_ONE_DATAS_USER_FILE_PATH
from scripts.logins.login_base import LoginBase
from scripts.redpackets.redpacket_base import RedpacketBase
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config

login_one_data_list = Base().read_user(TEST_ONE_DATAS_USER_FILE_PATH)


@ddt
class World_Question(unittest.TestCase):
    # 问卷红包测试类

    @classmethod
    def setUpClass(cls):
        login_actual = LoginBase().login(do_config("username", "A"))
        login_token = login_actual.json()["token"]
        dumpchoice_actual = RedpacketBase().question_dumpchoice(login_token)
        for i in range(13):
            subject_id, answer_list = RedpacketBase().get_question_id(login_token)
            answer_id = random.choice(answer_list)
            actual = RedpacketBase().do_question(login_token, subject_id, answer_id)
        actual = RedpacketBase().question_release(login_token)
        cls.questionnaire_id = actual.json()["questionnaire_id"]

    @classmethod
    def tearDownClass(cls):
        print("结束")

    @data(*login_one_data_list)
    def test_case_01(self, login_data):
        login_data = json.dumps(login_data)
        login_actual = LoginBase().login(login_data)
        vip = login_actual.json()["user_info"]["vip"]
        if vip >= 10:
            login_token = login_actual.json()["token"]
            joinanswer_actual = RedpacketBase().\
                get_question_joinanswer(login_token, self.questionnaire_id)

            choice_question_id_list = []
            answer_id_list = []
            choice_list = []
            print(joinanswer_actual.json())
            subject = joinanswer_actual.json()["subject"]
            for a in range(13):
                choice_question_id = subject[a]["choice_question_id"]
                choice_question_id_list.append(choice_question_id)
                answer_list = subject[a]["answer"]
                for c in range(len(answer_list)):
                    var = answer_list[c]["id"]
                    choice_list.append(var)
                answer_id = random.choice(choice_list)
                answer_id_list.append(answer_id)

            choice_question_id = ",".join(choice_question_id_list)
            answer_id = ",".join(answer_id_list)
            print(choice_question_id)
            print(answer_id)

            question_joinanswer_actual = RedpacketBase().question_joinanswer(login_token,
                                                                             self.questionnaire_id,
                                                                             choice_question_id,
                                                                             answer_id)
            print(question_joinanswer_actual.json())
        else:
            print("vip等级不够，现在等级：{}".format(vip))


if __name__ == '__main__':
    unittest.main()

