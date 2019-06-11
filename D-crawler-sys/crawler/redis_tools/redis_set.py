__all__=(
    "RedisSet",
)

import redis


class RedisSet:
    def __init__(self, redis_conn, name, namespace):
        self.__db = redis_conn
        self.key = '%s:%s' %(namespace, name)

    def add(self,item):
        self.__db.sadd(self.key,item)

    def remove(self,item):
        self.__db.srem(self.key,item)

    def is_member(self,item)->bool:
        return self.__db.sismember(self.key,item)
        