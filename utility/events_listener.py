from abc import ABC, abstractmethod

class EventsListener(ABC):        
    @abstractmethod
    def on_event(self, event):
        ...
