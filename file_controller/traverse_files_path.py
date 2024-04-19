import logging
import os

logger = logging.getLogger(__name__)


def traverse_files_path(file_path: str) -> []:
    logger.info(f'正在获取{file_path}下的文件')
    res = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            path = os.path.join(root, file)
            # print(path[len(file_path) + 1::])
            res.append(path[len(file_path) + 1::])
    return res
