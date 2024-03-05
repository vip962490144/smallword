# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import random

from scripts.handle_config import do_config
from scripts.handle_requests import HandleRequest
from scripts.logins.login_base import LoginBase


class DiscoverBase:
    # 发现页操作类

    # 比赛点赞
    def submit_like(self, token, data_list):
        # login_actual = Base().login(do_config("username", "A"))
        # login_token = login_actual.json()["token"]
        headers = {'content-type': 'application/json',
                   'authorization': 'Bearer ' + token}  # +token#需要的话 传输token 用来用户权限验证
        submit_url = do_config("api", "url") + "competition/like"

        # competition_id = random.rand(1261, 1262, 1263)

        # data_list = {"submit_id": 1261,'like_num': 22}
        send_res = HandleRequest()
        actual = send_res(method="post", url=submit_url, headers=headers, data=data_list, is_json=True)
        send_res.close()

        return actual

    # 获取比赛视频id列表
    def get_submit_id(self, token, competition_id):
        headers = {'content-type': 'application/json',
                   'authorization': 'Bearer ' + token}  # +token#需要的话 传输token 用来用户权限验证
        submit_url = do_config("api", "url") + \
                     "competition/submit_list?competition_id={}&pos=0&limit=100".format(competition_id)
        send_res = HandleRequest()
        actual = send_res(method="get", url=submit_url, headers=headers)
        send_res.close()

        submit_list = actual.json()["list"]
        submit_id_list = []
        w = 0
        for i in submit_list:
            submit_id = i["submit_id"]
            submit_id_list.append(submit_id)
            w += 1

        print(submit_id_list)
        print(len(submit_id_list))

        # print(submit_id_list)
        # print(w)

        return actual

    # 获取比赛id
    def get_competition_id(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
                   "app-versioon": "2.9.15"}  # +token#需要的话 传输token 用来用户权限验证
        submit_url = do_config("api", "url") + "competition"

        send_res = HandleRequest()
        actual = send_res(method="get", url=submit_url, headers=headers)
        send_res.close()

        return actual

    # 提交比赛视频
    def competition_submit(self, token, data):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token,
                   "app-version": "2.9.15"}  # +token#需要的话 传输token 用来用户权限验证
        submit_url = do_config("api", "url") + "competition/submit"
        send_res = HandleRequest()
        actual = send_res(method="POST", url=submit_url, data=data, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 比赛后台审核列表
    def get_competition_check_list(self, token):
        headers = {'content-type': 'application/json',
                   'authorization': 'Bearer ' + token}  # +token#需要的话 传输token 用来用户权限验证
        submit_url = do_config("api", "url") + \
                     "backend/competition/check?pos=0&limit=100&status=1"
        send_res = HandleRequest()
        actual = send_res(method="GET", url=submit_url, headers=headers)
        send_res.close()

        return actual

    # 获取后台审核列表的比赛id
    def get_competition_id_list(self, token):
        actual = self.get_competition_check_list(token)
        competition_list = actual.json()["list"]
        competition_id_list = []
        for a in competition_list:
            competition_id = a["id"]
            competition_id_list.append(competition_id)

        return competition_id_list

    # 比赛后台审核
    def competition_check_list(self, token, competition_id):
        headers = {'content-type': 'application/json',
                   'authorization': 'Bearer ' + token}  # +token#需要的话 传输token 用来用户权限验证
        submit_url = do_config("api", "url") + "backend/competition/check"
        data_list = {"id": competition_id, "result": 1}
        send_res = HandleRequest()
        actual = send_res(method="PUT", url=submit_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 世界墙点赞
    def the_wall_like(self, the_wall_id, num, token):
        # +token#需要的话 传输token 用来用户权限验证
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        the_wall_url = do_config("api", "url") + "world_moment/{}/like".format(the_wall_id)
        da = {"id": the_wall_id, "num": num}
        send_res = HandleRequest()
        actual = send_res(method="post", url=the_wall_url, data=da, headers=headers)
        send_res.close()
        print(actual.json())
        return actual

    # 竞猜奖池
    def get_guess_diamond(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        guess_diamond_url = do_config("api", "url") + "guess/getdiamond"
        send_res = HandleRequest()
        actual = send_res(method="get", url=guess_diamond_url, headers=headers)
        send_res.close()
        return actual

    # 一键竞猜
    def random_guess(self, login_token, data_list):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + login_token}
        random_guess_url = do_config("api", "url") + "guess/batch_dobets"
        # random_guess_url = do_config("api", "url") + "guess/arr_guess"
        send_res = HandleRequest()
        actual = send_res(method="post", url=random_guess_url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 模块列表
    def get_modular_list(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "lifestyle/modular"
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 商户列表
    def get_merchant_list(self, token, modular_id):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + "lifestyle/merchant?" \
                                        "pos=0&limit=10&modular_id={}".format(modular_id)
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 随机给出一个模块id
    def get_modular_id(self, token):
        actual = self.get_modular_list(token)
        modular_list = actual.json()
        list_id = []
        for a in range(len(modular_list)):
            list_id.append(modular_list[a]["id"])

        return random.choice(list_id)

    # 随机给出一个模块id
    def get_merchant_id(self, token, modular_id):
        actual = self.get_merchant_list(token, modular_id)
        moudle_list = actual.json()["list"]
        list_id = []
        for a in range(len(moudle_list)):
            list_id.append(moudle_list[a]["id"])

        return random.choice(list_id)

    # 打印此模块下所有方法名的方法
    def methods(self):
        return (list(
            filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self, m)),
                   dir(self))))

    # class_dict = {key: var for key, var in locals().items() if isinstance(var, type)}

    # 获取发布资格状态
    def photo_album_publish_status(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + 'photo_album/publish_status'
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 获取主题列表
    def get_photo_album(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + 'photo_album/topics_list?pos=0&limit=10'
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 随机取出一个主题列表
    def get_photo_album_topicid(self, token):
        actual = self.get_photo_album(token)
        print(actual)
        photo_album = actual.json()["list"]

        photo_album_list = []
        for var in range(len(photo_album)):
            id = photo_album[var]["id"]
            photo_album_list.append(id)

        photo_album_topicid = random.choice(photo_album_list)

        return photo_album_topicid

    # 创建写真集内容
    def create_photo_album(self, photo_album_topicid, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + 'photo_album'
        data_list = {"file_num": "3",
                     "context": "amet",
                     "topics": [
                         photo_album_topicid
                     ]
                     }

        send_res = HandleRequest()
        actual = send_res(method="POST", url=url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 申请写真集资格
    def apply_photo_album(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = "http://106.75.29.100:8081/" + "photo_album/apply"
        url = do_config("api", "url") + "photo_album/apply"
        data_list = {
            "file_num": "3",
            "introduce": "jaden",
            "money": "200",
            "context": "jaden"
        }

        send_res = HandleRequest()
        actual = send_res(method="POST", url=url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 点赞写真集
    def like_photo_album(self, photo_album_id, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + 'photo_album/like'
        data_list = {
            "id": photo_album_id,
            "num": "5000"
        }

        send_res = HandleRequest()
        actual = send_res(method="POST", url=url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 评论写真集
    def comment_photo_album(self, photo_album_id, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + 'photo_album/comment'
        data_list = {
            "id": photo_album_id,
            "context": "aliqua Lorem dolor ut"
        }

        send_res = HandleRequest()
        actual = send_res(method="POST", url=url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 获取设置写真集信息
    def get_photo_album_set_info(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + 'photo_album/set_info'
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 设置写真集
    def put_photo_album(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + 'photo_album/set_info'
        data_list = {
            "money": "11111",
            "introduce": "aliqua Lorem dolor ut"
        }

        send_res = HandleRequest()
        actual = send_res(method="put", url=url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 获取某个用户的写真集列表
    def get_photo_album_user(self, user_id, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + 'photo_album'
        data_list = {"user_id": user_id}
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, data=data_list, headers=headers, is_json=True)
        send_res.close()

        return actual

    # 获取自己的写真集列表
    # photo_album/my_list
    def get_my_photo_album(self, token):
        headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + token}
        url = do_config("api", "url") + 'photo_album/my_list?limit=202'
        send_res = HandleRequest()
        actual = send_res(method="get", url=url, headers=headers, is_json=True)
        send_res.close()

        return actual

    # /photo_album/subscribe
    #


if __name__ == '__main__':
    obj = DiscoverBase()
    a_login_actual = LoginBase().login(do_config("username", "A"))
    a_login_token = a_login_actual.json()["token"]
    # actual = obj.get_modular_list(a_login_token)
    actual = obj.get_submit_id(a_login_token, 488)
    print(actual.json())

    # token = LoginBase().get_backend_token(do_config("admin", "A"))
    # actual = obj.get_competition_check_list(token)
    # print(actual.json()["list"])
    #
    # actual = obj.get_my_photo_album(a_login_token)
    # print(actual.json())
    # print(len(actual.json()["list"]))

id_list = ['2341', '2340', '2339', '2338', '2337', '2336', '2335', '2334', '2333',
           '2332', '2331', '2330', '2329', '2328', '2327', '2326', '2325', '2324',
           '2323', '2322', '2321', '2320', '2319', '2318', '2317', '2316', '2315',
           '2314', '2313', '2312', '2311', '2310', '2309', '2308', '2307', '2306',
           '2305', '2304', '2303', '2302', '2301', '2300', '2299', '2298', '2297',
           '2296', '2295', '2294', '2293', '2292', '2291', '2290', '2289', '2288',
           '2287', '2286', '2285', '2284', '2283', '2282', '2281', '2280', '2279',
           '2278', '2277', '2276', '2275', '2274', '2273', '2272', '2271', '2270',
           '2269', '2268', '2267', '2266', '2265', '2264', '2263', '2262', '2261',
           '2260', '2239', '2259', '2258', '2257', '2256', '2255', '2254', '2253',
           '2252', '2251', '2250', '2249', '2248', '2247', '2246', '2245', '2244',
           '2243']
