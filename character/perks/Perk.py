from __future__ import annotations
from typing import Dict, TYPE_CHECKING
import os
if TYPE_CHECKING:
    from mechanics.buffs import Ability

class Perk:
    max_level = 3

    abilities = {}

    def __init__(self, name, level_to_abils: Dict[int, Ability], cost_factor=1, icon = os.path.join("icons", "params", "64", "strange_perk.png") ):
        self.name = name
        self.current_level = 0
        self.level_to_abils = level_to_abils
        self.cost_factor = cost_factor
        self.icon = icon

    @property
    def abils(self):
        return self.level_to_abils.get(self.current_level, list())

    def __repr__(self):
        if self.current_level == 0:
            return f"learn {self.name[self.current_level+1]}"
        return f"{self.name[self.current_level]}"