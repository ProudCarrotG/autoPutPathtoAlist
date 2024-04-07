import logging
import sys
from importlib import import_module

import requests

from config.config_check import check_alist_addr, check_token

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

        # self.print_config()

    def get_config_by_settings(self):
        """
        读取settings.py
        :return:
        """
        try:
            module = import_module("settings")
        except Exception as e:
            logger.error(e)
            module = import_module("test_settings")
        for key in dir(module):
            if key.isupper():
                self.setting[key] = getattr(module, key)

        self.config_check()
        # self.print_config()

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
            logger.error("连接服务器失败")
            sys.exit(404)

        self[self.ALIST_TOKEN] = res.json()["data"]["token"]
        logger.info(f"token:{self[self.ALIST_TOKEN]}")
