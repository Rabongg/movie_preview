from database.redis_client import RedisClient
import logging

class RedisPublisher:

    def __init__(self, topic):
        self.topic = topic
        self.client = RedisClient.get_instance()

    def publish_message(self, message):
        try:
            logging.info(f"Publishing message to {self.topic}")
            logging.info(f"message: {message}")
            self.client.publish(self.topic, message=message)
        except Exception:
            logging.exception('Publishing message failed!')
            raise
        else:
            logging.info('Message published successfully!')
