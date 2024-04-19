import logging
from time import time

import requests

logger = logging.getLogger(__name__)


# 检测alist地址
def check_alist_addr(addr: str):
    payload = ''
    headers = {}

    try:
        start_time = time()
        res = requests.get(addr + '/ping', headers=headers)
        end_time = time()
        if res.status_code == 200:
            logger.info('连接alist服务器成功')
            logger.info(f"当前延迟:{int((end_time - start_time) * 1000)}ms")
            return True
        else:
            logger.error('连接失败')
            return False
    except Exception as e:
        logger.error(e)
        logger.error('连接失败')
        return False


# 检测alist的token
def check_token(addr: str, token: str):
    headers = {
        'Authorization': token,
    }
    try:
        res = requests.get(addr + '/api/me', headers=headers)

        if res.status_code == 200 and res.json()['code'] == 200:
            logger.info('用户认证成功')
            logger.info('当前用户信息:' + str(res.json()))
        else:
            logger.error('用户认证失败')
    except Exception as e:
        logger.error(e)
        logger.error('用户认证失败')
