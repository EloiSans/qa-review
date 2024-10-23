import pika
from architecture.hex.port.event_queue import EventQueuePort

class RabbitMQAdapter(EventQueuePort):
    def __init__(self, host: str, port: int):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()

    def publish(self, queue_name: str, message: dict):
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=str(message))

    def consume(self, queue_name: str, callback):
        self.channel.queue_declare(queue=queue_name)

        def _callback(ch, method, properties, body):
            callback(body.decode())

        self.channel.basic_consume(queue=queue_name, on_message_callback=_callback, auto_ack=True)
        self.channel.start_consuming()
