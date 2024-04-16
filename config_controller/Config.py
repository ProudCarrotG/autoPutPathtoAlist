import logging
import os.path
import sys
import yaml
from importlib import import_module

import requests

from config_controller.config_check import check_alist_addr, check_token

logger = logging.getLogger(__name__)


# 设置管理类
class Config:
    """
    设置类
    """

    FILES_PATH = "FILES_PATH"
    ALIST_SERVER = "ALIST_SERVER"
    ALIST_PORT = "ALIST_PORT"
    ALIST_PATH = "ALIST_PATH"
    ALIST_TOKEN = "ALIST_TOKEN"
    ALIST_DOMAIN = "ALIST_DOMAIN"
    ALIST_HTTPS = "ALIST_HTTPS"
    USE_DOMAIN = "USE_DOMAIN"
    ADDR = "addr"
    ALIST_USERNAME = "ALIST_USERNAME"
    ALIST_PASSWORD = "ALIST_PASSWORD"
    USER_TIMEOUT = 'USER_TIMEOUT'

    setting = dict()

    # 默认值
    def __init__(self):
        self.setting["FILES_PATH"] = "/files"
        self.setting["ALIST_SERVER"] = "localhost"
        self.setting["ALIST_PORT"] = "5244"
        self.setting["ALIST_PATH"] = "/"
        self.setting["ALIST_TOKEN"] = ""
        self.setting["ALIST_DOMAIN"] = ""
        self.setting["ALIST_HTTPS"] = 0
        self.setting["USE_DOMAIN"] = 0
        self.setting["ALIST_USERNAME"] = ""
        self.setting["ALIST_PASSWORD"] = ""
        self.setting["USER_TIMEOUT"] = None

        # self.print_config()

    def __get_by_yaml(self, path: str):
        try:
            file = open(path, 'rb')
            config = yaml.safe_load(file)
        except Exception as e:
            logger.error(e)
            return False

        for key, val in config.items():
            if key.isupper():
                self.setting[key] = val

        return True

    def __get_by_py(self, path: str):
        abspath = os.path.abspath(path)
        module_dir = os.path.dirname(abspath)
        if module_dir not in sys.path:
            sys.path.append(module_dir)
        file_name = os.path.basename(abspath)
        logger.debug(module_dir)

        module_name = file_name.split(".")[0]
        try:
            logger.debug(module_name)

            module = import_module(module_name)
            # module = import_module('configs.test_settings', package='autoPutPathtoAlist')
        except Exception as e:
            logger.error(e)
            return False

        for key in dir(module):
            if key.isupper():
                self.setting[key] = getattr(module, key)

        return True

    def get_by_file(self, path: str):
        config_type = os.path.splitext(path)[-1]
        res = ''
        if config_type == ".yaml":
            res = self.__get_by_yaml(path)
        elif config_type == '.py':
            res = self.__get_by_py(path)
        else:
            logger.error("未知类型的配置文件")
            res = False

        self.config_check()
        return res

    def _get_config_by_settings(self, path: str):
        """
        读取settings.yaml
        :return:
        """
        config_type = os.path.splitext(path)[-1]
        if config_type == '.yaml':
            config = ''
            try:
                file = open(path, 'rb')
                config = yaml.safe_load(file)
            except Exception as e:
                logger.error(e)

            for key, val in config.items():
                if key.isupper():
                    self.setting[key] = val

            # self.print_config()
        elif config_type == '.py':
            name = os.path.split(path)
            module = ''
            try:
                module = os.path.splitext(name[0])
            except Exception as e:
                logger.error(e)

            for key in dir(module):
                if key.isupper():
                    self.setting[key] = getattr(module, key)
        else:
            logger.error("未知的配置文件类型")
            logger.debug(config_type)
            return False
        self.config_check()
        return True

    def print_config(self):
        """
        打印当前的设置
        :return:
        """
        for key, val in self.setting.items():
            logger.info(f"{key}: {val}")
        logger.info(self["addr"])
        logger.info("----------------")

    def __getitem__(self, item):
        if item == "addr":
            return self.get_addr()

        return self.setting[item]

    def __setitem__(self, key, value):
        if key not in self.setting:
            raise KeyError(f"key {key} not in setting")
        self.setting[key] = value

    def get_addr(self):
        """
        获取地址
        :return:string地址
        """
        addr = ""
        if self.setting["USE_DOMAIN"] == 0:
            addr = self.setting["ALIST_SERVER"] + ":" + self.setting["ALIST_PORT"]
            return self.ishttps(addr)
        else:
            addr = self.setting["ALIST_DOMAIN"]
            return self.ishttps(addr)

    def ishttps(self, addr):
        """
        判断是否使用https
        :param addr: 待处理的初始地址
        :return: string添加好协议头的地址
        """
        if "://" not in addr:
            if self[Config.ALIST_HTTPS] == 0:
                return "http://" + addr
            else:
                return "https://" + addr
        else:
            return addr

    def config_check(self):
        """
        检测当前配置是否正确
        :return:
        """
        check_alist_addr(self[self.ADDR])

        if self[self.ALIST_TOKEN] == "" and self[self.ALIST_USERNAME] != '':
            self.alist_login()
        check_token(self.get_addr(), self[self.ALIST_TOKEN])

    def alist_login(self):
        """
        登录alist以获取token
        :return:
        """
        addr = self.get_addr()
        username = self[self.ALIST_USERNAME]
        password = self[self.ALIST_PASSWORD]

        logger.debug(username)
        logger.debug(password)

        headers = {"Content-Type": "application/json"}
        body = {"username": username, "password": password}

        res = ""
        try:
            res = requests.post(addr + "/api/auth/login", json=body, headers=headers)

            if res.status_code == 200 and res.json()["code"] == 200:
                logger.info("登录成功")
                logger.info(f"登录信息:{res.json()}")
            else:
                logger.error("登陆失败")
                logger.error(f"失败信息{res.json()}")
                sys.exit(400)
        except Exception as e:
            logger.error(e)
            logger.error("验证用户信息时，连接服务器失败")
            logger.info("出现此条信息时，请检查服务器域名最后有没有多余的'/'")
            sys.exit(404)

        self[self.ALIST_TOKEN] = res.json()["data"]["token"]
        logger.info(f"token:{self[self.ALIST_TOKEN]}")
