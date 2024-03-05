# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
# from scripts.Base import Base
from scripts.clubs.club_base import ClubBase
from scripts.handle_config import do_config
from scripts.logins.login_base import LoginBase
from scripts.partys.party_base import PartyBase


def equal_clubs():
    login_actual = LoginBase().login(do_config("username", "A"))
    login_token = login_actual.json()["token"]
    print(login_actual.json()["user_info"]["id"])
    print(login_token)
    my_create_clubs_list, my_join_clubs_list = ClubBase().get_clubs_list(login_token)
    club_list1 = []
    for i in range(len(my_join_clubs_list)):
        var = my_join_clubs_list[i]["id"]
        club_list1.append(var)
    print(club_list1)

    party_list1 = []
    for i in range(len(my_create_clubs_list)):
        var = my_create_clubs_list[i]["id"]
        party_list1.append(var)

    print(party_list1)

    login_actual = LoginBase().login(do_config("username", "B"))
    login_token = login_actual.json()["token"]

    my_create_clubs_list, my_join_clubs_list = ClubBase().get_clubs_list(login_token)
    party_list2 = []
    for i in range(len(my_join_clubs_list)):
        var = my_join_clubs_list[i]["id"]
        party_list2.append(var)

    print(party_list2)

    a = []
    for i in party_list1:
        for b in party_list2:
            if i == b:
                if len(a) < 10:
                    a.append(i)
                else:
                    break
    print("A与B相同的10个俱乐部,为{}".format(a))


def equal_party():
    login_actual = LoginBase().login(do_config("username", "A"))
    login_token = login_actual.json()["token"]
    all_party_actual = PartyBase().get_all_party(login_token)
    # print(all_party_actual.json())
    party_list = all_party_actual.json()["list"]
    party_list1 = []
    for i in range(len(party_list)):
        var = party_list[i]["id"]
        party_list1.append(var)

    # print(party_list1)
    login_actual = LoginBase().login(do_config("username", "B"))
    login_token = login_actual.json()["token"]
    all_party_actual = PartyBase().get_all_party(login_token)
    # print(all_party_actual.json())
    party_list = all_party_actual.json()["list"]
    party_list2 = []
    for i in range(len(party_list)):
        var = party_list[i]["id"]
        party_list2.append(var)

    # print(party_list2)

    a = []
    for i in party_list1:
        for b in party_list2:
            if i == b:
                if len(a) < 10:
                    a.append(i)
                else:
                    break
    print("A与B相同的10个聚会,为{}".format(a))


if __name__ == '__main__':
    equal_clubs()
    equal_party()
