import base64
import json
import os.path
import sys
import urllib.parse
from typing import Union

import requests

import config.Config
import settings
import http.client

from importlib import import_module


def pretty_json(data):
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    json_data = json.loads(data)
    return json.dumps(json_data, ensure_ascii=False, indent=4)


def upload_file(path, settings: dict):
    if not isinstance(path, str):
        raise TypeError("Path must be a string")

    path = os.path.abspath(path)
    file_name = os.path.split(path)[-1]

    with open(path, "rb") as file:
        conn = http.client.HTTPConnection("127.0.0.1:5244")
        payload = file.read()
        headers = {
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicHdkX3RzIjoxNzA1OTI4NzUyLCJleHAiOjE3MTI0MTAzNDgsIm5iZiI6MTcxMjIzNzU0OCwiaWF0IjoxNzEyMjM3NTQ4fQ.fSIBuDQ58EBj8wOI-YeIpSgsEWrHer133MdZejvN6_o",
            "File-Path": f'{urllib.parse.quote(settings["ALIST_PATH"])}/{file_name}',
            "As-Task": "true",
            "Content-Type": "text/plain",
        }

        conn.request("PUT", "/api/fs/put", payload, headers)
        response = conn.getresponse()
        data = response.read()
        print(pretty_json(data))


if __name__ == "__main__":
    # 日志
    import logging, coloredlogs

    coloredlogs.install(level=logging.DEBUG, stream=sys.stdout)

    # 读取设置
    config = config.Config.Config()
    config.get_config_by_settings()

    # upload_file(
    #     path="settings.py",
    #     settings=setting
    # )

    # requests.request("GET")
