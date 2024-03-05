# -*- coding: utf-8 -*-
import os

from configparser import ConfigParser

from scripts.constants import CONFIG_FILE_PATH, CONFIGS_DIR


class HandleConfig(ConfigParser):
    """
    定义处理配置文件的类
    """
    def __init__(self, filename=None):   # 对父类的构造方法进行拓展
        # 先调用父类的构造方法
        super().__init__()  # 重写或者拓展父类的构造方法，往往我们需要先调用父类的构造方法
        self.filename = filename

    def __call__(self, section="DEFAULT", option=None, is_eval=False, is_bool=False):
        """
        '对象()'这种形式，__call__方法会被调用
        :param section: 区域名
        :param option: 选项名
        :param is_eval: 为默认参数，是否进行eval函数转换，默认不转换
        :param is_bool: 选项所对应的值是否需要转化为bool类型，默认不转换
        :return:
        """
        self.read(self.filename, encoding="utf-8")  # 读取配置文件
        if option is None:
            # 一个对象(区域名)    # 能够获取此区域下的所有选项，构造出来的一个字典
            # 一个对象()  # 返回DEFAULT默认区域下的所有选项，构造成的一个字典
            return dict(self[section])

        if isinstance(is_bool, bool):
            if is_bool:
                # 一个对象(区域名, 选项名, is_bool=True)  # 将获取到的数据使用getboolean()方法来获取
                return self.getboolean(section, option)
        else:
            raise ValueError("is_bool必须是布尔类型")  # 手动抛异常

        data = self.get(section, option)
        # 如果获取到的数据为数字类型的字符型，自动转化为Python中数字类型
        if data.isdigit():  # 判断是否为数字类型的字符串
            return int(data)
        try:
            return float(data)  # 如果为浮点类型的字符串，则直接转换
        except ValueError:
            pass

        if isinstance(is_eval, bool):
            if is_eval:
                # 一个对象(区域名, 选项名, is_eval=True)  # 将获取到的数据使用eval函数进行转换
                return eval(data)
        else:
            raise ValueError("is_eval")  # 手动抛异常
        return data

    @classmethod
    def write_config(cls, data, filename):
        """
        将数据写入配置文件
        :param data:
        :param filename: 文件名
        :return:
        """
        one_config = cls()
        for key in data:
            one_config[key] = data[key]
        filename = os.path.join(CONFIGS_DIR, filename)
        with open(filename, "w", encoding="utf-8") as one_file:
            one_config.write(one_file)


do_config = HandleConfig(CONFIG_FILE_PATH)

if __name__ == '__main__':
    config = HandleConfig()
    pass
