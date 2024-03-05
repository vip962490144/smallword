# -*- coding:utf-8 -*-
# @Author   :Jaden.wang

import json
import os
import random
import time
import unittest
import base64

from filetype import filetype

from scripts.Base import Base
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase
from scripts.upload.ufile import file_type
from scripts.upload.ufile.postfile import postfile


class FileBase:

    # 上传世界墙文件
    @staticmethod
    def get_moment_id(token, moment_id):
        headers = {'content-type': 'application/json',
                   'authorization': 'Bearer ' + token}  # +token#需要的话 传输token 用来用户权限验证
        submit_url = do_config("api", "url") + "world_moment/file?" \
                                               "sort=1&moment_id={}&type=1".format(moment_id)
        data = {"type": 1, "duration": "10047", "mime_type": "image/png",
                "thumbnail_mime_type": "image/png"}
        send_res = HandleRequest()
        actual = send_res(method="POST", url=submit_url, data=data, headers=headers, is_json=True)
        send_res.close()
        return actual

    # 判断创建世界墙是否需要钻石
    @staticmethod
    def get_the_wall_diamond(token):
        headers = {'content-type': 'application/json',
                   'authorization': 'Bearer ' + token}  # +token#需要的话 传输token 用来用户权限验证
        url = do_config("api", "url") + "world_moment/diamond"
        send_res = HandleRequest()
        actual = send_res(method="GET", url=url, headers=headers)
        send_res.close()
        return actual

    # 创建世界墙
    @staticmethod
    def creat_the_wall(token, user_id):
        headers = {'content-type': 'application/json',
                   'authorization': 'Bearer ' + token}  # +token#需要的话 传输token 用来用户权限验证
        url = do_config("api", "url") + "world_moment"
        data = {"user_id": user_id, "context": "", "city": "上海", "location": "不列颠群岛", "file_num": 1}
        send_res = HandleRequest()
        actual = send_res(method="POST", url=url, data=data, headers=headers, is_json=True)
        send_res.close()
        return actual

    # 创建世界墙文件上传
    @staticmethod
    def create_post_file(token, data):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
                   "app-version": "2.9.15"}  # +token#需要的话 传输token 用来用户权限验证
        create_file_url = do_config("api", "url") + "file"
        send_res = HandleRequest()
        actual = send_res(method="POST", url=create_file_url, data=data, headers=headers, is_json=True)
        send_res.close()
        return actual

    # 告知文件上传结束，发布世界墙
    @staticmethod
    def put_file_end(token, file_id, moment_id=0, photo_album_id=0, sort=0, if_ifle=0):
        headers = {'content-type': 'application/json',
                   'authorization': 'Bearer ' + token}  # +token#需要的话 传输token 用来用户权限验证
        create_file_url = do_config("api", "url") + "file"
        if if_ifle == 0:
            data = {"file_id": file_id}
        elif if_ifle == "photo_album":
            data = {"file_id": file_id,
                    "photo_album": {
                        "id": photo_album_id,
                        "sort": sort,
                    },
                    "authentication": 0}
        else:
            data = {"file_id": file_id,
                    "world_moment": {
                        "id": moment_id,
                        "sort": 0,
                    },
                    "authentication": 0}

        send_res = HandleRequest()
        actual = send_res(method="PUT", url=create_file_url, data=data, headers=headers, is_json=True)
        send_res.close()
        return actual

    # 判断文件类型
    @staticmethod
    def get_file_type(work_path):
        # try:
        url = work_path
        work_path = os.path.basename(work_path)
        # 判断是不是..视频
        if work_path.endswith(('.mp4', '.mkv', '.avi', '.wmv', '.iso')):
            kind = filetype.guess(url)
            return kind.mime
        elif work_path.endswith(('.jpg', '.png', '.jpeg', '.bmp')):
            kind = filetype.guess(url)
            return kind.mime
        else:
            print("文件类型错误")
            exit()
        # except Exception as e:
        #     raise e
        #     print("文件类型错误")

    # 提交文件获取格式
    def get_file_data(self, localfile, file_name_type="图片"):
        if file_name_type == "图片":
            mime_photo_type = self.get_file_type(localfile)
            data_list = {'type': 1, 'width': 1000, 'height': 1000, 'mime_type': mime_photo_type}
            return data_list
        elif file_name_type == "视频":
            localfile1 = localfile[0]
            localfile2 = localfile[1]
            mime_photo_type = self.get_file_type(localfile1)
            mime_video_type = self.get_file_type(localfile2)
            data_list = {"type": 2, "duration": "10047", "mime_type": mime_video_type,
                         "thumbnail_mime_type": mime_photo_type}
            return data_list
        else:
            print("文件类型错误")
            exit()

    # 提交文件
    def file_submit(self, login_token, localfile, file_name_type="图片"):
        data_list = self.get_file_data(localfile=localfile, file_name_type=file_name_type)
        actual = FileBase().create_post_file(login_token, data_list)
        print(actual.json())
        if file_name_type == "图片":
            mime_photo_type = data_list["mime_type"]
            file_id = actual.json()["file_id"]
            signature = actual.json()["signature"]
            thumbnail_photo_url = "https://new-mini-world.cn-bj.ufileos.com/" + file_id + mime_photo_type
            postfile(thumbnail_photo_url, signature, file_id, localfile)
            return file_id

        elif file_name_type == "视频":
            localfile1 = localfile[0]
            localfile2 = localfile[1]
            mime_video_type = data_list["mime_type"]
            mime_photo_type = data_list["thumbnail_mime_type"]
            file_id = actual.json()["file_id"]
            signature = actual.json()["signature"]
            file_url = actual.json()["file_url"]
            thumbnail_id = actual.json()["thumbnail_id"]
            thumbnail_signature = actual.json()["thumbnail_signature"]
            thumbnail_url = actual.json()["thumbnail_url"]
            file_video_url = "https://new-mini-world.cn-bj.ufileos.com/" + file_id + mime_video_type
            thumbnail_photo_url = "https://new-mini-world.cn-bj.ufileos.com/" + file_id + mime_photo_type
            ret, resp = postfile(file_video_url, signature, file_id,  localfile1)
            print(resp)
            ret, resp = postfile(thumbnail_photo_url, thumbnail_signature, thumbnail_id, localfile2)
            print(resp)
            return file_id


if __name__ == '__main__':
    obj = FileBase()
    # B = {"mobile": "17775309964", "password": "123456"}
    # B = json.dumps(B)
    # login_actual = login(B)
    # login_token = login_actual.json()["token"]

    A = '{"mobile": "17621620738", "password": "123456"}'
    login_actual = LoginBase().login(A)
    login_token = login_actual.json()["token"]
    user_id = login_actual.json()["user_info"]["id"]

    localfile1 = r'D:\test.mp4'
    localfile2 = r'D:\test.png'
    # localfile1 = r'D:\viddd.mp4'
    # localfile2 = r'D:\viddd.gif'
    # localfile = r'D:\1.jpg'

    # data = obj.get_file_type(localfile1)
    # print(data)
    mime_video_type = obj.get_file_type(localfile1)
    mime_photo_type = obj.get_file_type(localfile2)

    data = {"type": 2, "duration": "10047", "mime_type": mime_video_type,
            "thumbnail_mime_type": mime_photo_type}

    print(data)
    actual = obj.get_the_wall_diamond(login_token)
    print(actual.json())
    actual = obj.creat_the_wall(login_token, user_id)
    print(actual.json())
    moment_id = actual.json()["id"]

    actual = obj.create_post_file(login_token, data)
    print(actual.json())
    file_id = actual.json()["file_id"]
    signature = actual.json()["signature"]
    file_url = actual.json()["file_url"]
    thumbnail_id = actual.json()["thumbnail_id"]
    thumbnail_signature = actual.json()["thumbnail_signature"]
    thumbnail_url = actual.json()["thumbnail_url"]
    file_video_url = "https://new-mini-world.cn-bj.ufileos.com/" + file_id + ".mp4"
    thumbnail_photo_url = "https://new-mini-world.cn-bj.ufileos.com/" + thumbnail_id + ".png"
    res, resp = postfile(file_video_url, signature, file_id, localfile1)
    print(resp)
    res, resp = postfile(thumbnail_photo_url, thumbnail_signature, thumbnail_id, localfile2)
    print(resp)
    actual = obj.put_file_end(login_token, file_id, moment_id)
    # print(actual.text)
    # print(file_url, thumbnail_url)
