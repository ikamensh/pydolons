from __future__ import annotations
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.buffs import Ability

class Perk:
    max_level = 3

    abilities = {}

    def __init__(self, level_to_abils: Dict[int, Ability]):
        self.current_level = 0
        self.level_to_abils = level_to_abils

    @property
    def abils(self):
        return self.level_to_abils.get(self.current_level, list())