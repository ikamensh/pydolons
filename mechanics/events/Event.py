from mechanics.events.EventsPlatform import EventsPlatform
from abc import abstractmethod


class Event:
    def __init__(self):
        self.interrupted = False
        EventsPlatform.process_event(self)

    @abstractmethod
    def resolve(self):
        raise NotImplementedError

    def check_conditions(self):
        return True










