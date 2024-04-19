import logging

import config_controller.name
import file_controller
from file_controller.upload_file import upload_files


def Controller(
        # addr: str,
        # token: str,
        # alist_path: str,
        # file_root: str,
        # files: [str],
        # user_timeout: int,
        config: dict
):
    while True:

        # fail_list, fail_msg, repeat_list = upload_files(addr, token, alist_path, file_root, files, user_timeout)
        fail_list, fail_msg, repeat_list = upload_files(config)

        if len(repeat_list) != 0:
            logging.info(f"重复的文件：")
            for i in repeat_list:
                logging.info(i)
            logging.info(
                "---------------------------------------------------------------"
            )

        if len(fail_list) != 0:
            logging.info(f"上传失败文件：")
            for file, msg in fail_msg:
                logging.info(f"{file}:{msg}")
            logging.info(
                "---------------------------------------------------------------"
            )

        op = ""
        if len(fail_list) == 0:
            op = "N"
        while op != "Y" and op != "N":
            op = input("输入Y尝试重新上传失败文件,输入N结束程序，输入S设置超时时间")
            logging.debug(op)

            if op == "y":
                op = "Y"
            if op == "n":
                op = "N"
            if op == 'S' or op == 's':
                user_timeout = int(input('(设置为-1，不会超时自动停止传输)超时时间：'))
                if user_timeout == -1:
                    user_timeout = None
                op = ''

        if op == "N":
            break
        if op == "Y":
            files = fail_list.copy()
            fail_msg.clear()
            fail_list.clear()
            logging.debug(files)

    return
