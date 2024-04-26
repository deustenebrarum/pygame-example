from abc import ABC, abstractmethod

class EventsListener(ABC):
    _listeners = list()
    
    def __init__(self):
        EventsListener._listeners.append(self)
    
    @classmethod
    def dispatch(cls, event):
        for listener in cls._listeners:
            listener.on_event(event)
        
    @abstractmethod
    def on_event(self, event):
        ...