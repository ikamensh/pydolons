from __future__ import annotations
import copy

from game_objects import battlefield_objects
from character.masteries.Masteries import Masteries
from character.masteries.MasteriesEnumSimple import MasteriesEnum


from typing import Set, TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import BaseType, Unit, CharAttributes


class Character:
    def __init__(self, base_type : BaseType):
        from character.perks.everymans_perks.everymans_perk_tree import everymans_perks

        self.base_type = base_type
        self._masteries = Masteries()
        self.temp_attributes = None
        self.temp_masteries = None

        self.perk_trees = [everymans_perks()]
        self._unit = battlefield_objects.Unit(base_type, masteries=self.masteries)
        self.gold = 10000

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
    def masteries(self):
        return self.temp_masteries or self._masteries

    @property
    def attributes(self):
        return self.temp_attributes or self.base_type.attributes

    @property
    def attributes_count(self) -> int:
        return Masteries.achieved_level(self.xp) + 48

    @property
    def free_attribute_points(self) -> int:
        return self.attributes_count - sum(self.attributes.values())

    @property
    def free_xp(self) -> int:
        return self.xp - self.masteries.total_exp_spent - sum( pt.spent_xp for pt in self.perk_trees)


    def increase_attrib(self, attrib_enum: CharAttributes) -> None:
        if self.free_attribute_points <= 0:
            return

        if self.temp_attributes is None :
            self.temp_attributes = copy.copy(self.base_type.attributes)
        self.temp_attributes[attrib_enum] += 1
        self.update_unit()

    def reduce_attrib(self, attrib_enum: CharAttributes) -> None:
        if self.temp_attributes is None :
            return
        self.temp_attributes[attrib_enum] -= 1
        self.update_unit()


    def increase_mastery(self, mastery: MasteriesEnum) -> None:
        if not mastery in self.masteries_can_go_up:
            return

        if self.temp_masteries is None:
            self.temp_masteries = copy.deepcopy(self.masteries)

        self.temp_masteries.level_up(mastery)
        self.update_unit()


    def commit(self):
        if self.temp_attributes:
            self.base_type.attributes = self.temp_attributes
            self.temp_attributes = None

        if self.temp_masteries:
            self._masteries = self.temp_masteries
            self.temp_masteries = None

        self.update_unit()


    def reset(self):
        self.temp_attributes = None
        self.temp_masteries = None
        self.update_unit()

    def update_unit(self):
        self._unit.update(self.base_type_prelim, self.masteries)
        for pt in self.perk_trees:
            for a in pt.all_abils:
                self._unit.add_ability(a)

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
        return self._unit


    @property
    def xp(self):
        return self.unit.xp
