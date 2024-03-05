# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
from scripts.Base import Base
from scripts.activities_and_discoveries.discover_base import DiscoverBase
from scripts.activities_and_discoveries.file_base import FileBase
from scripts.constants import TEST_USER_DATAS_USER100_FILE_PATH, TEST_USER_DATAS_USER3_FILE_PATH
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase
from scripts.upload.ufile.postfile import postfile


# 提交世界比赛视频
def read_user(username):
    """
    :param username: 文件名，绝对路径
    :return:
    """
    with open(username, "r") as file:
        data_list = []
        while True:
            mystr = file.readline().strip('\n')     # 表示一次读取一行
            if not mystr:
            # 读到数据最后跳出，结束循环。数据的最后也就是读不到数据了，mystr为空的时候
                return data_list
            mobile = mystr
            data = {"mobile": mobile}
            data_list.append(data)


# login_one_data_list = read_user(TEST_USER_DATAS_USER3_FILE_PATH)
login_one_data_list = Base().read_user(TEST_USER_DATAS_USER3_FILE_PATH)

list_token = []
#
# for i in range(len(login_one_data_list)):
#     login_data = login_one_data_list[i]
#     phone = login_data["mobile"]
#     LoginBase().captcha(phone)
#     actual = LoginBase().register(phone)
#     token = actual.json()["token"]
#     list_token.append(token)
#
# submit_id_list = []
# #
# for token in list_token:
#     actual = DiscoverBase().get_competition_id(token)
#     # print(actual.json())
#     competition_id = actual.json()["id"]
# #
# #     # localfile = r'D:\video-photo\1.jpg'
# #     # localfile = r'D:\video-photo\1.png'
#     localfile1 = r'D:\test1119.mp4'
#     localfile2 = r'D:\test1119.png'
#
#     mime_video_type = FileBase().get_file_type(localfile1)
#     mime_photo_type = FileBase().get_file_type(localfile2)
#
#     data = {"type": 2, "duration": "10047", "mime_type": mime_video_type,
#                     "thumbnail_mime_type": mime_photo_type}
#
#     actual = FileBase().create_post_file(token, data)
#     # print(actual.json())
#     file_id = actual.json()["file_id"]
#     signature = actual.json()["signature"]
#     file_url = actual.json()["file_url"]
#     thumbnail_id = actual.json()["thumbnail_id"]
#     thumbnail_signature = actual.json()["thumbnail_signature"]
#     thumbnail_url = actual.json()["thumbnail_url"]
#     file_video_url = "https://new-mini-world.cn-bj.ufileos.com/" + file_id + mime_video_type
#     thumbnail_photo_url = "https://new-mini-world.cn-bj.ufileos.com/" + file_id + mime_photo_type
#     ret, resp = postfile(file_video_url, signature, file_id,  localfile1)
#     # print(resp)
#     ret, resp = postfile(thumbnail_photo_url, thumbnail_signature, thumbnail_id, localfile2)
#     # print(resp)
#     actual = FileBase().put_file_end(token, file_id, if_ifle=True)
#     # print(actual.json())
#     data_list = {"competition_id": competition_id, "file_id": file_id}
#     actual = DiscoverBase().competition_submit(token, data_list)
#     print(actual.json())
#     submit_id = actual.json()["submit_id"]
#     submit_id_list.append(submit_id)

token = LoginBase().get_backend_token(do_config("admin", "A"))

competition_id_list = DiscoverBase().get_competition_id_list(token)

for a in competition_id_list:
    actual = DiscoverBase().competition_check_list(token, a)
    print(actual.json())

# print(submit_id_list)
