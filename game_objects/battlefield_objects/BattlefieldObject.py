from abc import ABC

class BattlefieldObject(ABC):

    @property
    def health(self):
        raise NotImplementedError

    def lose_health(self, amount, source = None):
        raise NotImplementedError