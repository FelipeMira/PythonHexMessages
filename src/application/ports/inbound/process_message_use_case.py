from abc import ABC, abstractmethod

class ProcessMessage(ABC):
    @abstractmethod
    def run(self, message):
        pass