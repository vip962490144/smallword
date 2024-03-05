from multiprocessing import Pool
import time, random, os

from scripts.Base import Base
from scripts.constants import TEST_ONE_DATAS_USER_FILE_PATH
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest


# def func(n):
#     pid = os.getpid()
#     print('进程%s正在处理第%d个任务'%(pid,n),'时间%s'%time.strftime('%H-%M-%S'))
#     time.sleep(2)
#     res = '处理%s'%random.choice(['成功','失败'])
#     return res


# 登录
def login(phone="17621620001", password="a123456"):
    # 返回登录的token
    headers = {'content-type':'application/json', 'authorization': 'Bearer '}
    login_url = do_config("api", "url") + "users/login"
    # print("手机号{}".format(phone))
    data = {"mobile":phone,
            "password": password,
            "device": "android",
            "language": "ch",
            "area_code": "+86",
            "device_no": "test",
            "phone_type": "9500",
            "system": "28",
            "idfa": "test"}
    send_res = HandleRequest()
    actual = send_res(method="post", url=login_url, headers=headers, data=data, is_json=True)
    send_res.close()
    return actual


# 获取问卷题目
def get_question(token):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    get_question_url = do_config("api", "url") + "question/choice?language=0"
    res = HandleRequest()
    actual = res(method="get", url=get_question_url, headers=headers)
    res.close()
    return actual


# 获取问卷id和答案id
def get_question_id(token):
    actual = get_question(token)
    subject_id = actual.json()["subject"]["subject_id"]
    answer = actual.json()["subject"]["answer"]
    answer_list = []
    for i in range(len(answer)):
        var = answer[i]["id"]
        answer_list.append(var)
    return subject_id, answer_list


# 填写问卷
def do_question(token, subject_id, answer_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    do_question_url = do_config("api", "url") + "question/dochoice"
    data = {"subject_id": subject_id, "answer_id": answer_id}
    res = HandleRequest()
    actual = res(method="post", url=do_question_url, data=data, headers=headers, is_json=True)
    res.close()
    return actual


# 发布问卷红包
def question_release(token):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    question_release_url = do_config("api", "url") + "question/release"
    data = {"money":"1000"}
    res = HandleRequest()
    actual = res(method="post", url=question_release_url, data=data, headers=headers, is_json=True)
    res.close()
    return actual


# 中断问卷填写发布
def question_dumpchoice(token):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    question_dumpchoice_url = do_config("api", "url") + "question/dumpchoice"
    res = HandleRequest()
    actual = res(method="GET", url=question_dumpchoice_url, headers=headers)
    res.close()
    return actual


# 获取世界问卷题目
def get_question_joinanswer(token, questionnaire_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    question_joinanswer_url = do_config("api", "url") + \
                              "question/joinanswer?questionnaire_id={}".format(questionnaire_id)
    res = HandleRequest()
    actual = res(method="GET", url=question_joinanswer_url, headers=headers)
    res.close()
    return actual


# 填写世界问卷题目
def question_joinanswer(token, questionnaire_id, choice_question_id, answer_id):
    headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
    question_joinanswer_url = do_config("api", "url") + \
                              "question/joinanswer?questionnaire_id={}".format(questionnaire_id)
    data = {"choice_question_id": choice_question_id, "answer_id": answer_id}
    res = HandleRequest()
    actual = res(method="post", url=question_joinanswer_url, data=data, headers=headers, is_json=True)
    res.close()
    return actual

# 答题
def get_answr(token, questionnaire_id):
    joinanswer_actual = get_question_joinanswer(token, questionnaire_id)
    choice_question_id_list = []
    answer_id_list = []
    choice_list = []
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

    question_joinanswer_actual = question_joinanswer(token,
                                                     questionnaire_id,
                                                     choice_question_id,
                                                     answer_id)
    return question_joinanswer_actual.text


def foo(info):
    print(info)     # 传入值为进程执行结果


if __name__ == '__main__':
    login_one_data_list = Base().read_user(TEST_ONE_DATAS_USER_FILE_PATH)
    p = Pool(40)
    li = []
    t4 = 0
    list_token = []
    for i in range(len(login_one_data_list)):
        login_data = login_one_data_list[i]
        phone = login_data["mobile"]
        password = login_data["password"]
        login_actual = login(phone, password)
        token = login_actual.json()["token"]
        vip = login_actual.json()["user_info"]["vip"]
        if vip >= 10:
            list_token.append(token)

    login_actual = login("17621620032", "a123456")
    token = login_actual.json()["token"]
    dumpchoice_actual = question_dumpchoice(token)
    for i in range(13):
        subject_id, answer_list = get_question_id(token)
        answer_id = random.choice(answer_list)
        actual = do_question(token, subject_id, answer_id)
    actual = question_release(token)
    questionnaire_id = actual.json()["questionnaire_id"]
    # questionnaire_id = "1366"

    for var in list_token:
        # token = list_token[var]
        t1 = time.time()
        # 领取红包
        res = p.apply_async(get_answr, args=(var, questionnaire_id),
                            callback=foo)
        # 结果不会立刻返回，遇到阻塞，开启下一个进程，在这，
        # 相当于几乎同时出现8个打印结果（一个线程处理一个任务，处理完下个任务才能进来）
        li.append(res)
        t2 = time.time()
        t3 = t2-t1
        t4 += t3

    p.close()   # join之前需要关闭进程池
    p.join()    # 因为异步，所以需要等待池内进程工作结束再继续
    for i in li:
        print(i.get())  # i是一个对象，通过get方法获取返回值，而同步则没有该方法
    print("总耗时：{}".format(t4))
