#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scripts.handle_pymusql import HandleMysql
from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config
from scripts.constants import CONFIG_USER_FILE_PATH


def create_new_user(rename, pwd="123456"):
    """
    创建一个用户
    :param rename:
    :param pwd:
    :return:
    """
    handle_mysql = HandleMysql()
    send_request = HandleRequest()

    url = do_config("api", "url") + "/member/register"
    sql = "SELECT `Id` FROM future.`member` WHERE `MobilePhone`=%s"
    while True:
        mobilephone = handle_mysql.create_not_mobile()
        data = {"mobilephone": mobilephone, "pwd": pwd, "rename": rename}
        send_request(method="post",
                     url=url,
                     data=data)
        result = handle_mysql(sql=sql, arg=(mobilephone, ))
        if result:
            user_id = result["Id"]
            break

    user_dict = {
        rename: {
            "Id": user_id,
            "regname": rename,
            "mobilephone": mobilephone,
            "pwd": pwd
        }
    }

    handle_mysql.close()
    send_request.close()

    return user_dict


def genrate_users_config():
    """
    生成三个用户的信息，
    :return:
    """
    users_datas_dict = {}
    users_datas_dict.update(create_new_user("admin_user"))
    users_datas_dict.update(create_new_user("invest_user"))
    users_datas_dict.update(create_new_user("borrow_user"))
    do_config.write_config(users_datas_dict, CONFIG_USER_FILE_PATH)
    return users_datas_dict


if __name__ == '__main__':
    print(genrate_users_config())
    # do_config.write_config(genrate_users_config(), "user_message.conf")






