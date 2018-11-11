from __future__ import annotations
from typing import Dict, List
from character.perks import Perk


class PerkGroup:
    def __init__(self, perk_list: List[Perk], requirements: Dict[PerkGroup:int] = None):
        self.perk_list = perk_list
        self.requirements = requirements

    def requirements_matched(self):
        if not self.requirements:
            return True
        return all([k.total_level >= v for k, v in self.requirements.items()])

    @property
    def total_level(self):
        return sum([p.current_level for p in self.perk_list])

    def __repr__(self):
        return f"group of {self.perk_list}"