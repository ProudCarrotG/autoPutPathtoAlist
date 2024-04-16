import os

import coloredlogs
import logging
import sys

import main

logger = logging.getLogger(__name__)
coloredlogs.install(level=logging.INFO, stream=sys.stdout)


def search_config() -> []:
    res = []
    for root, dirs, files in os.walk(".\\configs"):
        for file in files:
            if os.path.splitext(file)[-1] == ".yaml" or os.path.splitext(file)[-1] == ".py":
                path = os.path.join(root, file)
                res.append(path)
    return res


def main_multi():
    config_list = search_config()

    logger.info('搜索到以下配置文件')
    idx = 0
    for config in config_list:
        logger.info(f'{idx}: {config}')
        idx = idx + 1

    logger.info('输入使用的配置文件编号; 输入-1依次运行所有配置文件')
    op = int(input('编号:'))
    if op != -1:
        main.main(config_list[op])
    else:
        for config in config_list:
            main.main(config)


if __name__ == '__main__':
    logger.debug(__package__)
    main_multi()
