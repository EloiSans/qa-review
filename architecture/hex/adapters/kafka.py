from kafka import KafkaProducer, KafkaConsumer
from architecture.hex.port.event_queue import EventQueuePort

class KafkaAdapter(EventQueuePort):
    def __init__(self, brokers: list):
        self.producer = KafkaProducer(bootstrap_servers=brokers)
        self.consumer = None

    def publish(self, queue_name: str, message: dict):
        self.producer.send(queue_name, value=str(message).encode('utf-8'))
        self.producer.flush()

    def consume(self, queue_name: str, callback):
        self.consumer = KafkaConsumer(queue_name, bootstrap_servers=['localhost:9092'])
        for message in self.consumer:
            callback(message.value.decode('utf-8'))
