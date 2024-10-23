from abc import ABC, abstractmethod

class EventQueuePort(ABC):
    @abstractmethod
    def publish(self, queue_name: str, message: dict):
        """Publishes a message to the specified queue"""
        pass

    @abstractmethod
    def consume(self, queue_name: str, callback):
        """Consumes messages from the specified queue and handles them with a callback"""
        pass