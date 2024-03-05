# -*- coding: utf-8 -*-

from datetime import datetime
import os
import unittest

from libs import HTMLTestRunnerNew
from scripts.handle_config import do_config
from scripts.constants import CASES_DIR1, REPORTS_DIR, CONFIG_USER_FILE_PATH, CASES_DIR_GIFTS, CASES_DIR, BASE_DIR, \
    CASES_DIR_DIS, RED_DIR_DIS
from scripts.handle_user import genrate_users_config


# if not os.path.exists(CONFIG_USER_FILE_PATH):
#     genrate_users_config()

# # 用例路径
# case_path = os.path.join(os.getcwd(), "cases")
# # 报告存放路径
# report_path = os.path.join(os.getcwd(), "reports")


# 匹配case_path路径下的所有test开头的文件
def all_case():
    discover = unittest.defaultTestLoader.discover(RED_DIR_DIS,
                                                   pattern="test*.py",
                                                   top_level_dir=None)
    # print(discover)
    return discover


# data_discover = unittest.defaultTestLoader.discover(CASES_DIR_GIFTS, pattern="test_*.py",
#                                                     top_level_dir=CASES_DIR)

report_html_name = os.path.join(REPORTS_DIR, do_config("file path", "report_html_name"))
report_html_name_full = report_html_name + "_" + datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + ".html"
with open(report_html_name_full, mode='wb') as save_to_file:
    one_runner = HTMLTestRunnerNew.HTMLTestRunner(stream=save_to_file,
                                                  title=do_config("report", "title"),
                                                  verbosity=do_config("report", "verbosity"),
                                                  description=do_config("report", "description"),
                                                  tester=do_config("report", "tester"))
    one_runner.run(all_case())

if __name__ == '__main__':
    unittest.main()
    # print(BASE_DIR)
