# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
from scripts.activities_and_discoveries.discover_base import DiscoverBase
from scripts.logins.login_base import LoginBase

phone = 19956530035
LoginBase().captcha(phone)
actual = LoginBase().register(phone)
# actual = LoginBase().login(do_config("username", "C"))
login_token = actual.json()["token"]
# print(login_token)
user_id = actual.json()["user_info"]["id"]

photo_album_id = 109

DiscoverBase().like_photo_album(photo_album_id=photo_album_id, token=login_token)

for var in range(5000):
    DiscoverBase().comment_photo_album(photo_album_id=photo_album_id, token=login_token)


