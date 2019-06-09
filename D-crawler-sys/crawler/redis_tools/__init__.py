__all__=(
    "QUEUE",
)

import common
import redis
from .redis_queue import RedisQueue

c = common.args.redis_conf
host = c["host"]
port = c["port"]
decode_responses = c["decode_responses"]
queue_namespace = c["queue_namespace"]
queue_name = c["queue_name"]

connection_pool = redis.ConnectionPool(host=host, port=port)
# redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
redis_conn = redis.StrictRedis(
    connection_pool=connection_pool,
    decode_responses=decode_responses
)

QUEUE = RedisQueue(
    redis_conn = redis_conn,
    name = queue_name,
    namespace = queue_namespace
)
