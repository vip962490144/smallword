# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import argparse
from datetime import datetime
import json
import os
import threading
import time
import random

# import requests
# from scripts.constants import TEST_ONE_DATAS_USER_FILE_PATH
# import cv2

from scripts.constants import CONFIGS_DIR
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config


class Base:
    # 操作类

    # 获取10组竞猜列表
    def random_num(self, num):
        data_list = []
        var_list = []
        for var_1 in range(0, num):
            var_value1 = ""
            for var_2 in range(0, 5):
                var_value2 = random.randint(1, 5)
                var_value1 = var_value1 + str(var_value2)
            var_list.append(var_value1)
        data_list.append(var_list)
        key_num = "note_detail_arr",
        data_list = dict(zip(key_num, data_list))
        # data_list = var_list.update("note_detail_arr",data_list)
        return data_list

    # 读取文件
    @staticmethod
    def read_user(username):
        """
        :param username: 文件名，绝对路径
        :return:
        """
        with open(username, "r") as file:
            data_list = []
            while True:
                mystr = file.readline().strip('\n')     # 表示一次读取一行
                my_user = mystr.split(",")
                if not mystr:
                # 读到数据最后跳出，结束循环。数据的最后也就是读不到数据了，mystr为空的时候
                    return data_list
                mobile, password = my_user[0], my_user[1]
                data = {"mobile": mobile, "password": password}
                data_list.append(data)

    # 写入文件
    @staticmethod
    def write_config(mobile):
        """
        将数据写入配置文件
        :return:
        """
        boy_text = os.path.join(CONFIGS_DIR, "user_1k.txt")
        # boy = open("test_user_6.txt", 'a')
        # boy.write(str(mobile)+',123456\n')
        # boy.close()
        with open(boy_text, 'a') as boy:
            boy.write(str(mobile)+',123456\n')

    # 阿拉伯数字转汉字数字
    @staticmethod
    def num_to_char(num):
        num=str(num)
        num_dict={"0":u"零","1":u"一","2":u"二","3":u"三","4":u"四","5":u"五","6":u"六","7":u"七","8":u"八","9":u"九"}
        listnum=list(num)
        shu=[]
        for i in listnum:
            shu.append(num_dict[i])
        new_str = "".join(shu)
        return new_str

    # 处理视频保存帧数图片
    @staticmethod
    def parse_args():
        """
        Parse input arguments
        """
        parser = argparse.ArgumentParser(description='Process pic')
        parser.add_argument('--input', help='video to process', dest='input', default=None, type=str)
        parser.add_argument('--output', help='pic to store', dest='output', default=None, type=str)
        # default为间隔多少帧截取一张图片
        parser.add_argument('--skip_frame', dest='skip_frame', help='skip number of video', default=100,
                            type=int)  # 此处可更改提取帧的间隔
        args = parser.parse_args(
            ['--input', r'D:\test1119.mp4', '--output', r'D:\video-photo'])    # 此处添加路径，input为输入视频的路径 ，output为输出存放图片的路径
        return args

    # 处理视频保存帧数图片
    # @staticmethod
    # def process_video(i_video, o_video, num):
    #     cap = cv2.VideoCapture(i_video)
    #     num_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    #     expand_name = '.png'
    #     if not cap.isOpened():
    #         print("Please check the path.")
    #     cnt = 0
    #     count = 0
    #     while 1:
    #         ret, frame = cap.read()
    #         cnt += 1
    #         #  how many frame to cut
    #         if cnt % num == 0:
    #             count += 1
    #             cv2.imwrite(os.path.join(o_video, str(count) + expand_name), frame)
    #         if not ret:
    #             break


if __name__ == '__main__':
    obj = Base()
    args = obj.parse_args()
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    print('Called with args:')
    print(args)
    # obj.process_video(args.input, args.output, args.skip_frame)







