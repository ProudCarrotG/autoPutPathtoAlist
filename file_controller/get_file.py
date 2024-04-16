import logging, coloredlogs
import os

import requests

logger = logging.getLogger(__name__)


def get_file(addr: str, token: str, alist_path: str, file_path: str):
    """
    查询alist服务器在该路径下是否有这个文件
    :param alist_path: alist服务器的目录
    :param addr: http://服务器地址:端口
    :param token: alist的用户token
    :param file_path: 服务器上的文件相对路径
    :return: 是否查询到
    """
    url = addr + "/api/fs/get"
    path = os.path.join(alist_path, file_path)
    logger.debug(alist_path)
    logger.debug(file_path)
    logger.debug(f"path:{path}")

    header = {"Authorization": token}
    body = {"path": path}

    try:
        res = requests.post(url=url, json=body, headers=header)
        if res.json()["code"] == 500:
            logger.warning(f"未能在alist服务器上查询到文件{path}")
            return False
        elif res.json()["code"] == 200:
            logger.info(f"成功查询到文件{path}")
            return True
        else:
            logger.error("查询alist服务器文件时出现预期外错误")
            exit(1)
    except Exception as e:
        logger.error("查询alist服务器文件时服务器响应超时")
        logger.error(e)
        exit(1)
