from abc import ABC, abstractmethod


class TurnsManager(ABC):

    @abstractmethod
    def add_unit(self, unit):
        raise NotImplemented

    @abstractmethod
    def remove_unit(self, unit):
        raise NotImplemented

    @abstractmethod
    def get_next(self):
        raise NotImplemented
