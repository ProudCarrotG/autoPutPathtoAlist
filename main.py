import json
import sys
import config.Config
from file_controller.traverse_files_path import traverse_files_path
from file_controller.upload_file import upload_files


def pretty_json(data):
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    json_data = json.loads(data)
    return json.dumps(json_data, ensure_ascii=False, indent=4)


# def upload_file(path, settings: dict):
#     if not isinstance(path, str):
#         raise TypeError("Path must be a string")
#
#     path = os.path.abspath(path)
#     file_name = os.path.split(path)[-1]
#
#     with open(path, "rb") as file:
#         conn = http.client.HTTPConnection("127.0.0.1:5244")
#         payload = file.read()
#         headers = {
#             "Authorization": "",
#             "File-Path": f'{urllib.parse.quote(settings["ALIST_PATH"])}/{file_name}',
#             "As-Task": "true",
#         }
#
#         conn.request("PUT", "/api/fs/put", payload, headers)
#         response = conn.getresponse()
#         data = response.read()
#         print(pretty_json(data))


if __name__ == "__main__":
    # 日志
    import logging, coloredlogs

    coloredlogs.install(level=logging.DEBUG, stream=sys.stdout)

    # 读取设置
    config = config.Config.Config()
    config.get_config_by_settings()

    files = traverse_files_path(config[config.FILES_PATH])
    logging.debug(config[config.FILES_PATH])
    upload_files(config.get_addr(), config[config.ALIST_TOKEN], config[config.ALIST_PATH], config[config.FILES_PATH],
                 files)

    # upload_file(
    #     path="test_settings.py",
    #     settings=setting
    # )

    # requests.request("GET")
