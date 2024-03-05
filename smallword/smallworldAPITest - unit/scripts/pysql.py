# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import pymysql

from scripts.handle_config import do_config

connect_one = pymysql.connect(host=do_config("mysql", "host"),
                              user=do_config("mysql", "user"),
                              passwd=str(do_config("mysql", "password")),
                              db=do_config("mysql", "db"),
                              port=do_config("mysql", "port"),
                              charset=do_config("mysql", "charset"))

cursor = connect_one.cursor()


sql_1 = "SELECT * FROM invest LIMIT 0, 10;"
sql_2 = "SELECT VERSION()"

result1 = cursor.execute(sql_2)
data = cursor.fetchone()
print("Database version : %s " % data)
# connect_one.commit()

cursor.close()
