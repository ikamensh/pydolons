from abc import ABC

class BattlefieldObject(ABC):

    @property
    def health(self):
        raise NotImplementedError