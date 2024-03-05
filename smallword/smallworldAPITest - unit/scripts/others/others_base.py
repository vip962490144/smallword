# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest


class OthersBase:
    """
    其他操作类
    """

    # 获取排行
    def get_ranking(self, login_token, rank=None):
        # 获取登录token
        if rank == "实力榜" or rank is None:
            type_id = 3
        elif rank == "魅力榜":
            type_id = 2
        else:
            type_id = 3
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        rank_end_url = "ranking? type={}&pos=0&limit=10".format(type_id)
        rank_url = do_config("api", "url") + rank_end_url
        send_res = HandleRequest()
        actual = send_res(method="get", url=rank_url, headers=headers)
        send_res.close()

        return actual

    # 获取用id对应榜单的积分
    def get_user_ranking(self, login_token, user_id, rank=None):
        ranking_actual = self.get_ranking(login_token, rank)
        ranking_list = ranking_actual.json()["list"]
        for var in ranking_list:
            if int(user_id) == int(var["user_id"]):
                return var["amount"]

        amount = 0
        return amount
        # return print("user_id,{}此用户不在榜单中".format(user_id))
