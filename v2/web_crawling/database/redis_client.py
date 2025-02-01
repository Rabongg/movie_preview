import redis

class RedisClient:
    _instance = None

    @staticmethod
    def get_instance():
        if RedisClient._instance is None:
            RedisClient._instance = redis.Redis(host='localhost', port=6379, db=0)
        return RedisClient._instance