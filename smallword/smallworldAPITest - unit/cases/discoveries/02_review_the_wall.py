# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
from scripts.partys.party_base import PartyBase
from scripts.user_info.user_base import UserBase


data_list = {"longitude": "1.405222", "latitude": "1.16237"}

token = "03e0c4f813d42240fbaae7c2b84a14e46161772c"
UserBase().put_users_location(token, data_list)

lat = data_list["latitude"]
lon = data_list["longitude"]
party_id = 8190
actual = PartyBase().party_signup(token, party_id, lat=lat, lon=lon)
print(actual.text)
