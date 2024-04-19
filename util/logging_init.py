import logging
import os
from sys import stdout

import coloredlogs

logger = logging.getLogger(__name__)


def logging_init() -> None:
    if os.getenv('TEST'):
        coloredlogs.install(level=logging.DEBUG, stream=stdout)
        logger.debug('当前环境为开发、测试环境')
    else:
        coloredlogs.install(level=logging.INFO, stream=stdout)
        logger.info("当前环境为用户环境")
