from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from DreamGame import DreamGame

class Event:
    def __init__(self, game: DreamGame, fire: bool=True):
        self.interrupted = False
        self.game = game
        if fire:
            self.fire()

    def fire(self) -> None:
        if not self.game is None:
            self.game.events_platform.process_event(self)

    @abstractmethod
    def resolve(self) -> None:
        raise NotImplementedError

    def check_conditions(self) -> bool:
        return True
