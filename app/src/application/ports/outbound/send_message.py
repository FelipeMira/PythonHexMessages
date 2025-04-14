from abc import ABC, abstractmethod

class SendMessage(ABC):
    @abstractmethod
    def can_queue(self, message):
        pass

    @abstractmethod
    def send(self, message):
        pass