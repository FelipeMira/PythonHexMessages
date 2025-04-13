from abc import ABC, abstractmethod

class PersistorMessage(ABC):
    @abstractmethod
    def can_database(self, message):
        pass

    @abstractmethod
    def save(self, message):
        pass