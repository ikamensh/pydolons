from abc import abstractmethod
import my_context


class Event:
    def __init__(self, fire=True):
        self.interrupted = False
        if fire:
            self.fire()

    def fire(self):
        my_context.the_game.events_platform.process_event(self)

    @abstractmethod
    def resolve(self):
        raise NotImplementedError

    def check_conditions(self):
        return True
