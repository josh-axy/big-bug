__all__=(
    "QUEUE",
    "CLOSE_SET"
)

import common
# import redis
from .redis_queue import RedisQueue
from .redis_set import RedisSet

c = common.args.redis_conf
host = c["host"]
port = c["port"]
decode_responses = c["decode_responses"]
namespace = c["namespace"]
queue_name = c["queue_name"]
close_set_name = c["close_set_name"]

if c["single_node_mode"]:
    import redis
    connection_pool = redis.ConnectionPool(host=host, port=port)
    # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
    redis_conn = redis.StrictRedis(
        connection_pool=connection_pool,
        decode_responses=decode_responses
    )
    redis_nodes = [{'host':host,'port':port}]

else:
    import rediscluster
    redis_nodes = c["master_nodes"]
    # redis_conn = rediscluster.StrictRedisCluster(host=host,port=port)
    redis_conn = rediscluster.StrictRedisCluster(
        startup_nodes=redis_nodes,
        decode_responses=decode_responses
    )

QUEUE = RedisQueue(
    redis_conn = redis_conn,
    name = queue_name,
    namespace = namespace
)

CLOSE_SET = RedisSet(
    redis_conn = redis_conn,
    name = close_set_name,
    namespace = namespace
)
