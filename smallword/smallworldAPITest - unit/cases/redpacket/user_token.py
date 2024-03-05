#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: xubin
# @Date  : 2020/11/16

import requests
import threading
import time

token_file_name = 'token.txt'
user_file_name = 'test_user.txt'
##抽奖接口
lucky_url = 'http://106.75.11.161:9082/mallProduct/initiate_lucky_draw'
##登录接口
login_url = "http://106.75.11.161:9082/users/login"

# 写入文档
def write(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write('\n')


# 清空文档
def truncate_file(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()


# 读取文档
def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt


def token_txt():
    txt =[]
    filename = user_file_name
    file = open(filename)
    for line in file:
        sr = line.strip(' \n') #去重| 空格 换行

        txt.append(sr) #写入列表
        pass  # do something
    file.close()
    return  txt


def login(phone="17621620001", password="a123456"):
    # 返回登录的token
    headers = {'content-type': 'application/json', 'authorization': 'Bearer '}
    # print("手机号{}".format(phone))
    data = {"mobile": phone,
            "password": password,
            "device": "android",
            "language": "ch",
            "area_code": "+86",
            "device_no": "test",
            "phone_type": "9500",
            "system": "28",
            "idfa": "test"}
    res = requests.post(url=login_url, headers=headers, json=data)
    print(res.status_code)
    token = res.json()['token']
    ##获取的token写入文件备用
    write(token_file_name,token)
    return res


def main():

    ##清空文件
    truncate_file(token_file_name)

    # 执行次数
    tasks_number = int(input("enter number:"))

    # 获取token
    token = token_txt()

    """创建启动线程"""
    print("启动时间：",time.time())
    for i in range(tasks_number):

        ##获取手机号
        tokens = token[i].split(',',1)
        t_sing = threading.Thread(target=login,args=(tokens[0],tokens[1]))
        t_sing.start()
    print("结束时间：", time.time())

if __name__ == '__main__':
    main()