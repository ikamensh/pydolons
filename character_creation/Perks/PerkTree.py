
from typing import List

from character_creation.Perks import PerkGroup

class PerkTree:
    def __init__(self, perk_groups: List[PerkGroup]):
        self.perk_groups = perk_groups