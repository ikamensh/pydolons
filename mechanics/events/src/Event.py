from abc import abstractmethod


class Event:
    def __init__(self, game, fire=True):
        self.interrupted = False
        self.game = game
        if fire:
            self.fire()

    def fire(self):
        self.game.events_platform.process_event(self)

    @abstractmethod
    def resolve(self):
        raise NotImplementedError

    def check_conditions(self):
        return True
