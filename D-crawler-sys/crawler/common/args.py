__all__=(
    "ip",
    "port",
    "driver_cnt",
    "max_driver_cnt",
    "min_driver_cnt",
)


from . import env_args
from .path import get_config_path
import json

def get_crawler_config():
    p = get_config_path("crawler-conf.json")
    with open(p,"r") as fr:
        _json = json.load(fr)
    return _json

_json = get_crawler_config()
ip = _json["ip"]
port = _json["port"]
driver_cnt = _json["driver_cnt"]
max_driver_cnt = _json["max_driver_cnt"]
min_driver_cnt = _json["min_driver_cnt"]
