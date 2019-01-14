import copy

from game_objects.battlefield_objects import BaseType, Unit, CharAttributes
from character.masteries.Masteries import Masteries
from character.masteries.MasteriesEnumSimple import MasteriesEnum

from character.perks.everymans_perks.everymans_perk_tree import everymans_perks

from typing import List, Set

class Character:
    def __init__(self, base_type : BaseType):
        self.base_type = base_type
        self.masteries = Masteries()
        self._unit = Unit(base_type, masteries=self.masteries)

        self.temp_attributes = None
        self.temp_masteries = None

        self.perk_trees = [everymans_perks()]

        self.gold = 0

    @property
    def masteries_can_go_up(self) -> Set[MasteriesEnum]:
        result = set()

        mastery_map = self.temp_masteries or self.masteries

        for mastery in MasteriesEnum:
            cost_up, *_ = mastery_map.calculate_cost(mastery)
            if self.free_xp >= cost_up:
                result.add(mastery)

        return result

    @property
    def attributes_count(self) -> int:
        return Masteries.achieved_level(self.xp) + 48

    @property
    def free_attribute_points(self) -> int:
        if self.temp_attributes:
            return self.attributes_count - sum(self.temp_attributes.values())
        else:
            return self.attributes_count - sum(self.base_type.attributes.values())

    @property
    def free_xp(self) -> int:
        if self.temp_masteries:
            masteries_xp =  self.temp_masteries.total_exp_spent
        else:
            masteries_xp = self.masteries.total_exp_spent

        return self.xp - masteries_xp - sum( pt.spent_xp for pt in self.perk_trees)


    def increase_attrib(self, attrib_enum: CharAttributes) -> None:
        if self.free_attribute_points <= 0:
            return

        assert attrib_enum in CharAttributes
        if self.temp_attributes is None :
            self.temp_attributes = copy.copy(self.base_type.attributes)
        self.temp_attributes[attrib_enum] += 1

    def reduce_attrib(self, attrib_enum: CharAttributes) -> None:
        assert attrib_enum in CharAttributes
        if self.temp_attributes is None :
            return
        self.temp_attributes[attrib_enum] -= 1


    def increase_mastery(self, mastery: MasteriesEnum) -> None:
        if not mastery in self.masteries_can_go_up:
            return

        if self.temp_masteries is None:
            self.temp_masteries = copy.copy(self.masteries)

        self.temp_masteries.level_up(mastery)


    def commit(self):
        if self.temp_attributes:
            self.base_type.attributes = self.temp_attributes
            self.temp_attributes = None

        if self.temp_masteries:
            self.masteries = self.temp_masteries
            self.temp_masteries = None


    def reset(self):
        self.temp_attributes = None
        self.temp_masteries = None

    @property
    def base_type_prelim(self):
        if not self.temp_attributes:
            return self.base_type
        else:
            cpy = copy.copy(self.base_type)
            cpy.attributes = self.temp_attributes
            return cpy


    @property
    def unit(self) -> Unit:
        self._unit.update(self.base_type_prelim, masteries=self.temp_masteries or self.masteries)
        for pt in self.perk_trees:
            for a in pt.all_abils:
                self._unit.add_ability(a)
        return self._unit

    @property
    def xp(self):
        return self.unit.xp
