from scripts.backend.backend_base import BackendBase
from scripts.clubs.club_base import ClubBase
from scripts.logins.login_base import LoginBase
import json
from scripts.handle_config import do_config


class Club_apply():
    # 获取登录的token
    def login(self, login_data):
        login_data = json.dumps(login_data)
        login_actual = LoginBase().login(login_data)
        token = login_actual.json()["token"]
        return token

    # 修改用户钻石，确保不会因为俱乐部钻石不足，导致俱乐部被封禁
    def put_diamond(self, use_id):
        login_token = LoginBase().get_backend_token(do_config("admin", "C"))
        data_list = {"user_id": use_id, "diamond": "1000000"}
        BackendBase().updata_userinfo(login_token, data_list)

    # 正常申请加入俱乐部
    def club_apply(self):
        # 申请俱乐部
        actual1 = ClubBase().Apply_club(self.login(login_data), datalist)
        # 获取俱乐部申请列表
        actual2 = ClubBase().Club_invite_application(self.login(login_data))
        # 获取申请俱乐部成功之后的返回的ID
        ID1 = actual1.json()["id"]
        # 获取俱乐部列表的ID
        ID2_list = actual2.json()["list"]
        # 获取俱乐部的申请列表
        list = []
        for ID2 in ID2_list:
            list.append(ID2["id"])

        # 判断返回的ID在俱乐部列表中
        if ID1 in list:
            print("pass" + "----正常申请加入俱乐部")
        else:
            print("false" + "----正常申请加入俱乐部")

    # 加入俱乐部数量超出限制
    def case01(self):
        # 申请俱乐部
        login_data["mobile"] = 19956530034
        actual1 = ClubBase().Apply_club(self.login(login_data), datalist)
        if actual1.json()["error_message"] == "Max Club Num":
            print("pass" + "----正常申请加入俱乐部--APP内达到的最大值")
        else:
            print("false" + "----正常申请加入俱乐部--APP内达到的最大值")
            print(actual1.json())

        login_data["mobile"] = 18646767878
        actual1 = ClubBase().Apply_club(self.login(login_data), datalist)
        if actual1.json()["error_message"] == "Club Num Limit":
            print("pass" + "----正常申请加入俱乐部--VIP内达到的最大值")
        else:
            print("false" + "----正常申请加入俱乐部--VIP内达到的最大值")
            print(actual1.json())

    # 性别受限
    def case02(self):
        pass

    # 已加入该俱乐部
    def case03(self):
        login_data["mobile"] = 17622220103
        datalist["club_id"] = 5828
        actual1 = ClubBase().Apply_club(self.login(login_data), datalist)
        if actual1.json()["error_message"] == "Already In Club":
            print("pass" + "----已加入该俱乐部")
        else:
            print("false" + "----已加入该俱乐部")
            print(actual1.json())

    # 俱乐部被封禁
    def case04(self):
        datalist["club_id"] = 8343
        actual1 = ClubBase().Apply_club(self.login(login_data), datalist)
        if actual1.json()["error_message"] == "Club Banned":
            print("pass" + "----俱乐部被封禁")
        else:
            print("false" + "----俱乐部被封禁")
            print(actual1.json())

    # 俱乐部用户数量超出限制
    def case05(self):
        datalist["club_id"] = 8342
        actual1 = ClubBase().Apply_club(self.login(login_data), datalist)
        if actual1.json()["error_message"] == "User Num Limit":
            print("pass" + "----俱乐部用户数量超出限制")
        else:
            print("false" + "----俱乐部用户数量超出限制")
            print(actual1.json())

    # 你是游客
    def case06(self):
        # 游客账号
        mobile = 19796767766
        # 获取短信验证码
        LoginBase().captcha(mobile)
        # 注册/登录账号
        token_actual = LoginBase().register(mobile)
        # 获取token
        token = token_actual.json()["token"]
        actual1 = ClubBase().Apply_club(token, datalist)
        if actual1.json()["error_message"] == "U R Tourist":
            print("pass" + "----你是游客")
        else:
            print("false" + "----你是游客")
            print(actual1.json())

    # 需要提交视频
    def case07(self):
        login_data["mobile"] = 19956530008
        datalist["club_id"] = 8353
        actual1 = ClubBase().Apply_club(self.login(login_data), datalist)
        if actual1.json()["error_message"] == "Invalid Param file_id":
            print("pass" + "----需要提交视频")
        else:
            print("false" + "----需要提交视频")
            print(actual1.json())

    # 视频不存在
    def case08(self):
        login_data["mobile"] = 19956530008
        datalist = {"club_id": 8353, "file_id": "ss22222"}
        actual1 = ClubBase().Apply_club(self.login(login_data), datalist)
        if actual1.json()["error_message"] == "file_id Not Found":
            print("pass" + "----视频不存在")
        else:
            print("false" + "----视频不存在")
            print(actual1.json())

    # 无此俱乐部
    def case09(self):
        datalist["club_id"] = "ss22222"
        actual1 = ClubBase().Apply_club(self.login(login_data), datalist)
        if actual1.json()["error_message"] == "Not Found":
            print("pass" + "----无此俱乐部")
        else:
            print("false" + "----无此俱乐部")
            print(actual1.json())


if __name__ == '__main__':
    # 测试账号
    login_data = {"mobile": "17622220102", "password": "123456"}
    datalist = {
        "club_id": "",
        "reason": "",
        "file_id": ""
    }
    # 获取用户的token
    Club_apply().login(login_data)

    # 申请加入俱乐部
    datalist["club_id"] = 5828  # 手机号：17622220101的俱乐部
    Club_apply().club_apply()

    # 加入俱乐部数量超出限制
    Club_apply().case01()

    # 性别受限  现在APP内没有该功能 暂时不做处理
    Club_apply().case02()

    # 已加入该俱乐部
    Club_apply().put_diamond(14575)
    Club_apply().case03()

    # 俱乐部已被封禁
    Club_apply().case04()

    # 俱乐部用户数量超出限制
    Club_apply().case05()

    # 你是游客
    Club_apply().case06()

    # 需要提交视频
    Club_apply().case07()

    # 需要提交视频
    Club_apply().case08()

    # 无此俱乐部
    Club_apply().case09()
