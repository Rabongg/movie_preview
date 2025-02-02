import redis
import os

class RedisClient:
    _instance = None

    @staticmethod
    def get_instance():
        if RedisClient._instance is None:
            redis_host = os.getenv("REDIS_HOST", "localhost")  # 기본값: localhost
            redis_port = int(os.getenv("REDIS_PORT", 6379))  # 기본값: 6379
            RedisClient._instance = redis.Redis(host=redis_host, port=redis_port, db=0)
        return RedisClient._instance