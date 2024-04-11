import json
import sys

from config.Config import Config
from file_controller.traverse_files_path import traverse_files_path
from file_controller.upload_file import upload_files, contorller


def pretty_json(data):
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    json_data = json.loads(data)
    return json.dumps(json_data, ensure_ascii=False, indent=4)


def main():
    # 日志
    import logging, coloredlogs

    coloredlogs.install(level=logging.DEBUG, stream=sys.stdout)

    # 读取设置
    config = Config()
    config.get_config_by_settings()

    files = traverse_files_path(config[config.FILES_PATH])
    logging.debug(config[config.FILES_PATH])
    contorller(
        addr=config.get_addr(),
        token=config[config.ALIST_TOKEN],
        alist_path=config[config.ALIST_PATH],
        file_root=config[config.FILES_PATH],
        files=files,
        user_timeout=config[config.USER_TIMEOUT],
    )


if __name__ == "__main__":
    main()
