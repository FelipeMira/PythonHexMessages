from abc import ABC, abstractmethod

class SendMessage(ABC):
    @abstractmethod
    def canQueue(self, message):
        pass

    @abstractmethod
    def send(self, message):
        pass