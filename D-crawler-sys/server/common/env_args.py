'''
    读取环境变量
'''

__all__=(
    "SEVER_ROOT_PATH",
    "CRAWLER_ROOT_PATH",
    "CONFIG_ROOT_PATH",
    "WEBDRIVER_PATH",
)


import os
import json
import ast
from collections.abc import Callable
# import filetype


_env = os.environ

# 获取环境变量，并通过func进行转换
# 增加 assert 步骤，防止环境变量不存在
def get_env(env_var: str, func: Callable = str):
    _env_var = _env.get(env_var)
    assert _env_var is not None
    result = func(_env_var)
    # print(f"env var ${env_var}: {result}")
    return result


SEVER_ROOT_PATH =\
    get_env("server_root_path")

CRAWLER_ROOT_PATH =\
    get_env("crawler_root_path")

CONFIG_ROOT_PATH =\
    get_env("config_root_path")

WEBDRIVER_PATH=\
    get_env("webdriver_path")