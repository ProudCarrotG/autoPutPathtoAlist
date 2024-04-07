import logging
import os.path
import sys


def path_spliter(path: str):
    res = []

    while path != '':
        res.append(os.path.split(path)[1])
        # logging.debug(f'forin:{os.path.split(path)}')
        path = os.path.split(path)[0]
        # logging.debug(f'forinpath:{path}')
    res.append(path)

    return res[::-1]


def path_adder(path1: str, path2: str):
    """
    :param path1:
    :param path2:
    :return:
    """
    path1 = path_spliter(path1)
    path2 = path_spliter(path2)
    logging.debug(f"path1:{path1}")
    logging.debug(f"path2:{path2}")
    res = ''
    for dir in path1 + path2:
        res = os.path.join(res, dir)
    os.path.sep.join([])
    return res


if __name__ == '__main__':
    import logging, coloredlogs

    coloredlogs.install(level=logging.DEBUG, stream=sys.stdout)

    # logging.debug(os.path.split('..\\files'))

    # print(os.path.split('\\..\\aa'))
    # logging.debug(path_spliter('..'))

    # logging.debug(path_adder('..\\files', '\\123'))
    logging.debug(os.path.join('..\\aa\\b\\dd\\','11\\33'))
