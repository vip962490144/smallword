# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import json
import random

from scripts.Base import Base
from scripts.activities_and_discoveries.discover_base import DiscoverBase
from scripts.activities_and_discoveries.file_base import FileBase
from scripts.backend.backend_base import BackendBase
from scripts.constants import TEST_USER_DATAS_USER100_FILE_PATH
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase
from scripts.upload.ufile.postfile import postfile


def read_user(username):
    """
    :param username: 文件名，绝对路径
    :return:
    """
    with open(username, "r") as file:
        data_list = []
        while True:
            mystr = file.readline().strip('\n')  # 表示一次读取一行
            if not mystr:
                # 读到数据最后跳出，结束循环。数据的最后也就是读不到数据了，mystr为空的时候
                return data_list
            mobile = mystr
            data = {"mobile": mobile}
            data_list.append(data)


# actual = LoginBase().login(do_config("username", "B"))
# login_token = actual.json()["token"]
# user_id = actual.json()["user_info"]["id"]
# print(user_id)


def application_approved():
    # 申请写真集资格
    actual = DiscoverBase().apply_photo_album(login_token)
    print(actual.json())
    photo_album_id = actual.json()["photo_album_id"]

    file_submit(photo_album_id)

    # 查询资格审核列表
    apply_list_id = BackendBase().get_user_photo_album_id(backend_token, user_id)
    print(apply_list_id)

    # 通过审核
    actual = BackendBase().put_photo_album_check_apply(backend_token, apply_list_id)
    print(actual.text)


def topic_query(login_token):
    # 新增主题
    # actual = BackendBase().photo_album_topics(backend_token)
    # print(actual.text)

    # 获取主题列表的主题
    # actual = LoginBase().login(do_config("username", "B"))
    # login_token = actual.json()["token"]
    # photo_album_topicid = 1

    # actual = DiscoverBase().get_photo_album(login_token)
    # print(actual.text)
    #
    photo_album_topicid = DiscoverBase().get_photo_album_topicid(login_token)
    print(photo_album_topicid)

    return photo_album_topicid


def file_submit(photo_album_id):
    localfile1 = r'D:\video-photo\1.jpg'
    localfile2 = r'D:\video-photo\2.jpg'
    localfile3 = r'D:\video-photo\3.jpg'
    # localfile = [r'D:\video-photo\1.jpg', r'D:\video-photo\2.jpg', r'D:\video-photo\3.jpg']
    # localfile = [r'D:\video-photo\1.png', r'D:\test.mp4']

    # for var in localfile:
    #     file_id = FileBase().file_submit(login_token, localfile=var, file_name_type="图片")
    #     actual = FileBase().put_file_end(login_token, file_id, photo_album_id=photo_album_id, sort=1, if_ifle="photo_album")
    #     print(actual.json())
    # mime_video_type = FileBase().get_file_type(localfile2)
    mime_photo_type = FileBase().get_file_type(localfile1)

    data1 = {'type': 1, 'width': 1000, 'height': 1000, 'mime_type': mime_photo_type}

    actual = FileBase().create_post_file(login_token, data1)
    print(actual.json())
    file_id = actual.json()["file_id"]
    signature = actual.json()["signature"]
    thumbnail_photo_url = "https://new-mini-world.cn-bj.ufileos.com/" + file_id + ".jpg"
    res, resp = postfile(thumbnail_photo_url, signature, file_id, localfile1)
    print(resp)
    actual = FileBase().put_file_end(login_token, file_id, photo_album_id=photo_album_id, sort=1, if_ifle="photo_album")
    print(actual.json())

    actual = FileBase().create_post_file(login_token, data1)
    print(actual.json())
    file_id = actual.json()["file_id"]
    signature = actual.json()["signature"]
    res, resp = postfile(thumbnail_photo_url, signature, file_id, localfile2)
    print(resp)
    actual = FileBase().put_file_end(login_token, file_id, photo_album_id=photo_album_id, sort=2, if_ifle="photo_album")
    print(actual.json())

    actual = FileBase().create_post_file(login_token, data1)
    print(actual.json())
    file_id = actual.json()["file_id"]
    signature = actual.json()["signature"]
    res, resp = postfile(thumbnail_photo_url, signature, file_id, localfile3)
    print(resp)
    actual = FileBase().put_file_end(login_token, file_id, photo_album_id=photo_album_id, sort=3, if_ifle="photo_album")
    print(actual.json())

# 获取文件所有用户账户
# login_one_data_list = read_user(TEST_USER_DATAS_USER100_FILE_PATH)
# list_data = json.loads(do_config("username", "A"))
# list_data = do_config("username", "A")
# print(list_data, type(list_data))
# login_one_data_list = [json.loads(do_config("username", "A")), json.loads(do_config("username", "B"))]
backend_token = LoginBase().get_backend_token(do_config("admin", "D"))
# login_one_data_list = [do_config("username", "A"), do_config("username", "B")]
# list_token = []
# list_user_id = []
# 登录，放入token
# for i in range(len(login_one_data_list)):
#     login_data = login_one_data_list[i]
#     phone = login_data["mobile"]
#     LoginBase().captcha(phone)
    # actual = LoginBase().register(phone)
    # actual = LoginBase().login(login_one_data_list[i])
    # token = actual.json()["token"]
    # user_id = actual.json()["user_info"]["id"]
    # list_token.append(token)
    # list_user_id.append(user_id)


# 自动创建写真集
# for var in range(len(list_token)):
#     login_token = list_token[var]
#     user_id = list_user_id[var]
# 15661101255
phone = 15661101255
LoginBase().captcha(phone)
actual = LoginBase().register(phone)
# actual = LoginBase().login(do_config("username", "C"))
login_token = actual.json()["token"]
# print(login_token)
user_id = actual.json()["user_info"]["id"]
try:
    # 申请资格
    application_approved()
except Exception as e:
    pass

for var in range(5):
    # 获取主题
    photo_album_topicid = topic_query(login_token)

    # 创建写真集内容
    actual = DiscoverBase().create_photo_album(photo_album_topicid, login_token)
    print(actual.json())
    photo_album_id = actual.json()["photo_album_id"]

    file_submit(photo_album_id)

    # 遍历查询内容审核列表
    photo_album_list_id = BackendBase().get_user_photo_album_list_id(backend_token, user_id)
    print(photo_album_list_id)

    # 内容通过审核
    actual = BackendBase().put_photo_album(backend_token, photo_album_list_id)
    print(actual.text)



