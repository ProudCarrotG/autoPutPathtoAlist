import copy
import logging
import os.path
import sys
import time
import urllib.parse
from typing import Union, IO

import requests
import requests_toolbelt
import tqdm


# def foo(a) :


class Callback:
    def __init__(self, file_path: str):
        self.pbar: Union[tqdm.tqdm, None] = None
        self.last_read = 0
        self.file_path = file_path

    def __call__(self, monitor):
        if self.pbar is None:
            self.pbar = tqdm.tqdm(
                total=monitor.len,
                mininterval=0.01,
                colour="blue",
                unit_scale=True,
                unit="b",
            )
            self.pbar.set_description(f"{self.file_path}上传进度")
        if monitor.bytes_read - self.last_read != 0:
            self.pbar.update(monitor.bytes_read - self.last_read)
        self.last_read = monitor.bytes_read

    def __del__(self):
        # pass
        if not self.pbar:
            self.pbar.close()


def upload_file(addr: str, token: str, alist_path: str, file_root: str, file_path: str) -> int and str:
    """
    通过config配置上传文件
    :param file_root: 本地文件的根目录
    :param addr: http://服务器地址:端口
    :param token: alist用户token
    :param alist_path: alist服务器的目标路径
    :param file_path: 文件路径;相对路径
    :return: state:
            # 0:成功
            # 1：失败
            # 2：重复
            msg错误信息
    """

    # test
    # state = input('state:')
    # msg = input('msg:')
    # return int(state), msg

    url = addr + "/api/fs/form"
    file_abspath = os.path.abspath(os.path.join(file_root, file_path))
    # logging.debug(f"path_adder(file_root,file_path):{path_adder(file_root, file_path)}")
    file_name = os.path.split(file_path)[1]

    if get_file(addr, token, alist_path, file_path):
        logging.warning("alist服务器上存在同路径同名文件")
        return 2, None
    else:
        try:
            logging.info(f"开始上传文件{file_abspath}")
            with open(file_abspath, "rb") as file:
                # 等待缓冲区信息输出
                time.sleep(0.1)
                e = requests_toolbelt.MultipartEncoder(
                    fields={"file": (file_name, file)}
                )
                m = requests_toolbelt.MultipartEncoderMonitor(
                    e,
                    Callback(file_path),
                )
                header = {
                    "Authorization": token,
                    "File-Path": f"{urllib.parse.quote(os.path.join(alist_path, file_path))}",
                    "Content-Type": m.content_type,
                    "Content-Length": str(os.path.getsize(file_abspath)),
                    # "As-Task": "true",
                }
                # file_controller.upload_file.finish = 0
                res = requests.put(url=url, data=m, headers=header)

            logging.debug(file_path)

            if res.json()["code"] == 200:
                logging.info(f"文件上传成功{file_abspath}")
                return 0, None
            else:
                logging.warning(f"文件上传失败{file_abspath}")
                logging.warning(res.json())
                return 1, res.json()

        except Exception as e:
            logging.error("服务器失效")
            logging.error(e)
            return 1, e


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
    logging.debug(alist_path)
    logging.debug(file_path)
    logging.debug(f"path:{path}")

    header = {"Authorization": token}
    body = {"path": path}

    try:
        res = requests.post(url=url, json=body, headers=header)
        if res.json()["code"] == 500:
            logging.warning(f"未能在alist服务器上查询到文件{path}")
            return False
        elif res.json()["code"] == 200:
            logging.info(f"成功查询到文件{path}")
            return True
        else:
            logging.error("查询alist服务器文件时出现预期外错误")
            exit(1)
    except Exception as e:
        logging.error("查询alist服务器文件时服务器响应超时")
        logging.error(e)
        exit(1)


def upload_files(addr: str, token: str, alist_path: str, file_root: str, files: [str]):
    fail_list = []
    fail_msg = []
    repeat_list = []

    while True:
        for file in files:
            status = None

            status, msg = upload_file(addr, token, alist_path, file_root, file)

            if status == 1:
                fail_list.append(file)
                fail_msg.append((file, msg))
            elif status == 2:
                repeat_list.append(file)
            elif status == 0:
                pass
            else:
                print(f'嗯？你怎么给我返回了一个我没定义的状态值？你有问题  state：{status}')

        if len(repeat_list) != 0:
            logging.info(f'本次运行出现的重复文件：')
            for i in repeat_list:
                logging.info(i)
            logging.info('---------------------------------------------------------------')

        if len(fail_list) != 0:
            logging.info(f'上传失败文件：')
            for file, msg in fail_msg:
                logging.info(f'{file}:{msg}')
            logging.info('---------------------------------------------------------------')

        op = ''
        if len(fail_list) == 0:
            op = 'N'
        while op != 'Y' and op != 'N':
            op = input('输入Y尝试重新上传失败文件,输入N结束程序')

            if op == 'y':
                op = 'Y'
            if op == 'n':
                op = 'N'

        if op == 'N':
            break
        if op == 'Y':
            files = fail_list.copy()
            fail_msg.clear()
            fail_list.clear()
            logging.debug(files)

    return
