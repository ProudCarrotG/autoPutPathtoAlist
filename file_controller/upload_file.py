import logging
import os.path
import sys
import urllib.parse
from time import time

import requests

from config.Config import Config
from util.path_spliter import path_adder


def upload_file(addr: str, token: str, alist_path: str, file_root: str, file_path: str):
    """
    通过config配置上传文件
    :param file_root: 本地文件的根目录
    :param addr: http://服务器地址:端口
    :param token: alist用户token
    :param alist_path: alist服务器的目标路径
    :param file_path: 文件路径;相对路径
    :return:
    """

    url = addr + '/api/fs/put'
    file_abspath = os.path.abspath(os.path.join(file_root, file_path))
    # logging.debug(f"path_adder(file_root,file_path):{path_adder(file_root, file_path)}")
    file_name = os.path.split(file_path)[1]

    header = {
        'Authorization': token,
        'File-Path': f"{urllib.parse.quote(os.path.join(alist_path, file_path))}"
    }

    if get_file(addr, token, alist_path, file_path):
        logging.warning("alist服务器上存在同路径同名文件")
    else:
        try:
            logging.info(f"开始上传文件{file_abspath}")
            res = requests.put(url=url, files=open(file_abspath, 'rb'), headers=header)
            # logging.debug(file_path)
            if res.json()['code'] == 200:
                logging.info(f"文件上传成功{file_abspath}")
            else:
                logging.warning(f"文件上传失败{file_abspath}")
                logging.warning(res.json())
        except Exception as e:
            logging.error("服务器失效")
            logging.error(e)


def get_file(addr: str, token: str, alist_path: str, file_path: str):
    """
    查询alist服务器在该路径下是否有这个文件
    :param alist_path: alist服务器的目录
    :param addr: http://服务器地址:端口
    :param token: alist的用户token
    :param file_path: 服务器上的文件相对路径
    :return: 是否查询到
    """
    url = addr + '/api/fs/get'
    path = os.path.join(alist_path, file_path)
    logging.debug(alist_path)
    logging.debug(file_path)
    logging.debug(f"path:{path}")

    header = {
        'Authorization': token
    }
    body = {
        'path': path
    }

    try:
        res = requests.post(url=url, json=body, headers=header)
        if res.json()['code'] == 500:
            logging.warning(f"未能在alist服务器上查询到文件{path}")
            return False
        elif res.json()['code'] == 200:
            logging.info(f"成功查询到文件{path}")
            return True
        else:
            logging.error("查询alist服务器文件时出现预期外错误")
            exit(1)
    except Exception as e:
        logging.error("查询alist服务器文件时服务器响应超时")
        logging.error(e)
        exit(1)


def upload_files(addr: str, token: str, alist_path: str, file_root: str, files: []):
    for file in files:
        upload_file(addr, token, alist_path, file_root, file)
    return
