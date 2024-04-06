import logging
import os.path
import urllib.parse
from time import time

import requests

from config.Config import Config


def upload_file(config: Config, file_path: str):
    """
    通过config配置上传文件
    :param config: 设置好的config
    :param file_path: 文件路径;相对路径绝对路径都可以
    :return:
    """

    url = config.get_addr() + '/api/fs/put'
    file_path = os.path.abspath(file_path)
    file_name = os.path.split(file_path)[-1]

    header = {
        'Authorization': config[config.ALIST_TOKEN],
        'File-Path': f'{urllib.parse.quote(config[config.ALIST_PATH])}/{file_name}'
    }

    if get_file(config, config[config.ALIST_PATH] + file_name):
        logging.warning("alist服务器上存在同路径同名文件")
    else:
        try:
            logging.info("开始上传文件")
            res = requests.put(url=url, files=open(file_path, 'rb'), headers=header)
            # logging.debug(file_path)
            if res.json()['code'] == 200:
                logging.info("文件上传成功")
            else:
                logging.warning("文件上传失败")
                logging.warning(res.json())
        except Exception as e:
            logging.error("服务器失效")
            logging.error(e)


def get_file(config: Config, file_path: str):
    """
    查询alist服务器在该路径下是否有这个文件
    :param config: 配置信息
    :param file_path: 服务器上的文件路径
    :return: 是否查询到
    """
    url = config.get_addr() + '/api/fs/get'
    header = {
        'Authorization': config[config.ALIST_TOKEN]
    }
    body = {
        'path': file_path
    }

    try:
        res = requests.post(url=url, json=body, headers=header)
        if res.json()['code'] == 500:
            logging.warning(f"未能查询到文件{file_path}")
            return False
        elif res.json()['code'] == 200:
            logging.info(f"成功查询到文件{file_path}")
            return True
        else:
            logging.error("查询alist服务器文件时出现预期外错误")
            exit(1)
    except Exception as e:
        logging.error("查询alist服务器文件时服务器响应超时")
        logging.error(e)
        exit(1)
