from abc import ABC, abstractmethod

class ExceptionHandlerStrategy(ABC):
    @abstractmethod
    def handle(self, exception, event):
        pass