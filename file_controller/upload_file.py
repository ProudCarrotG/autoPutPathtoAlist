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

from config_controller import name
from file_controller.get_file import get_file


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
        if self.pbar is not None:
            self.pbar.close()


def upload_file(
        # addr: str,
        # token: str,
        # alist_path: str,
        # file_root: str,
        file_path: str,
        # user_timeout: int,
        config: dict
) -> int and str:
    """
    通过config配置上传文件
    :param file_root: 本地文件的根目录
    :param addr: http://服务器地址:端口
    :param token: alist用户token
    :param alist_path: alist服务器的目标路径
    :param file_path: 文件路径;相对路径
    :param user_timeout:超时参数
    :return: state:
            # 0:成功
            # 1：失败
            # 2：重复
            msg错误信息
    """

    addr = config[name.ADDR]
    token = config[name.ALIST_TOKEN]
    alist_path = config[name.ALIST_PATH]
    file_root = config[name.FILES_PATH]
    file_path = file_path
    user_timeout = config[name.USER_TIMEOUT]

    # test
    # state = input('state:')
    # msg = input('msg:')
    # return int(state), msg

    url = addr + "/api/fs/form"
    file_abspath = os.path.abspath(os.path.join(file_root, file_path))
    # logging.debug(f"path_adder(file_root,file_path):{path_adder(file_root, file_path)}")
    file_name = os.path.split(file_path)[1]
    callback = Callback(file_path=file_path)

    if get_file(addr, token, alist_path, file_path):
        logging.warning("alist服务器上存在同路径同名文件")
        # conflict_state = confilict_controller()
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
                    # Callback(file_path),
                    callback=callback
                )
                header = {
                    "Authorization": token,
                    "File-Path": f"{urllib.parse.quote(os.path.join(alist_path, file_path))}",
                    "Content-Type": m.content_type,
                    "Content-Length": str(os.path.getsize(file_abspath)),
                    # "As-Task": "true",
                }
                # file_controller.upload_file.finish = 0
                res = requests.put(
                    url=url, data=m, headers=header, timeout=user_timeout
                )
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
            callback.__del__()
            return 1, e


def upload_files(
        # addr: str,
        # token: str,
        # alist_path: str,
        # file_root: str,
        # files: [str],
        # user_timeout: int,
        config: dict
):
    fail_list = []
    fail_msg = []
    repeat_list = []

    for file in config[name.files]:
        status = None

        status, msg = upload_file(
            # addr=config[name.ADDR],
            # token=config[name.ALIST_TOKEN],
            # alist_path=config[name.ALIST_PATH],
            # file_root=config[name.FILES_PATH],
            file_path=file,
            # user_timeout=config[name.USER_TIMEOUT],
            config=config
        )

        if status == 1:
            fail_list.append(file)
            fail_msg.append((file, msg))
        elif status == 2:
            repeat_list.append(file)
        elif status == 0:
            pass
        else:
            logging.error(
                f"嗯？你怎么返回了一个我没定义的状态值？你有问题  state：{status}"
            )

    return fail_list, fail_msg, repeat_list
