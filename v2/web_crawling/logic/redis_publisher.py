from database.redis_client import RedisClient

class RedisPublisher:

    def __init__(self, topic):
        self.topic = topic
        self.client = RedisClient.get_instance()

    def publish_message(self, message):
        self.client.publish(self.topic, message=message)
