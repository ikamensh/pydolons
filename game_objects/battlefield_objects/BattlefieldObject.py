from abc import ABC

class BattlefieldObject(ABC):

    last_uid = 0
    uid = None

    @property
    def health(self):
        raise NotImplementedError

    def lose_health(self, amount, source = None):
        raise NotImplementedError