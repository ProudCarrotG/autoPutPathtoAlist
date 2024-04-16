import json
import sys
import logging, coloredlogs

from config_controller.Config import Config
from file_controller.Controller import Controller
from file_controller.traverse_files_path import traverse_files_path

logger = logging.getLogger(__name__)
coloredlogs.install(level=logging.INFO, stream=sys.stdout)


def pretty_json(data):
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    json_data = json.loads(data)
    return json.dumps(json_data, ensure_ascii=False, indent=4)


def main(path: str):
    # 日志

    # 读取设置
    config = Config()
    # config.get_config_by_settings(path)
    config.get_by_file(path)
    logger.error(path)

    files = traverse_files_path(config[config.FILES_PATH])
    logging.debug(config[config.FILES_PATH])
    Controller(
        addr=config.get_addr(),
        token=config[config.ALIST_TOKEN],
        alist_path=config[config.ALIST_PATH],
        file_root=config[config.FILES_PATH],
        files=files,
        user_timeout=config[config.USER_TIMEOUT],
    )


if __name__ == "__main__":
    # main('.\\configs\\settings.yaml')
    main('.\\settings.py')
