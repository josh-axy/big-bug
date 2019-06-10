__all__=(
    "ip",
    "port",
    "driver_cnt",
    "max_driver_cnt",
    "min_driver_cnt",
    "redis_conf",
    "hdfs_conf",
    "hbase_conf",
    "zk_conf",
    # "hdfs_url",
    # "hbase_url",
)


from . import env_args
from .path import get_config_path
import json

def get_config(conf_file:str):
    p = get_config_path(conf_file)
    with open(p,"r") as fr:
        _json = json.load(fr)
    return _json

_json = get_config("crawler-conf.json")
ip = _json["ip"]
port = _json["port"]
driver_cnt = _json["driver_cnt"]
max_driver_cnt = _json["max_driver_cnt"]
min_driver_cnt = _json["min_driver_cnt"]

redis_conf = get_config("redis-conf.json")
hdfs_conf = get_config("hdfs-conf.json")
hbase_conf = get_config("hbase-conf.json")
zk_conf = get_config("zookeeper-conf.json")

# hdfs_url = "{}://{}:{}".format(
#     hdfs_conf["protocol"],
#     hdfs_conf["host"],
#     hdfs_conf["port"]
# )
# hbase_url = "{}{}".format(hdfs_url,hbase_conf["hbase_rootdir"])
