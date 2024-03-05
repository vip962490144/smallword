#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    filename = token_file_name
    file = open(filename)
    for line in file:
        sr = line.strip(' \n') #去重| 空格 换行

        txt.append(sr) #写入列表
        pass  # do something
    file.close()
    return txt

"""
开始抽奖
"""
def post_curl(token,gift_draw_id):
    da = {"gift_draw_id": gift_draw_id}
    headers = {"Authorization":"Bearer %s" % (token)}
    # r = requests.post(url,data=da)
    res = requests.request("post",lucky_url,json =da, headers=headers)
    print(res.status_code)
    # print(res.text)


def main():

    # 执行次数
    tasks_number = int(input("enter number:"))
    gift_draw_id = int(input("gift_draw_id number:"))

    token = token_txt()

    """创建启动线程"""
    print("启动时间：",time.time())
    for i in range(tasks_number):

        ##获取手机号
        t_sing = threading.Thread(target=post_curl,args=(token[i],gift_draw_id))
        t_sing.start()
    print("结束时间：", time.time())

if __name__ == '__main__':
    main()
