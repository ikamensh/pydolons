import copy

from game_objects.battlefield_objects import BaseType, Unit
from game_objects.battlefield_objects.Unit import CharAttributes
from character_creation.Masteries import Masteries, MasteriesEnum


class Character:
    def __init__(self, base_type : BaseType):
        self.base_type = base_type
        self.masteries = Masteries()
        self.xp_total = 500

        self.preliminary_attributes = None
        self.preliminary_masteries = None

    @property
    def masteries_can_go_up(self):
        result = set()

        mastery_map = self.preliminary_masteries or self.masteries

        for mastery in MasteriesEnum:
            cost_up, *_ = mastery_map.calculate_cost(mastery)
            if self.free_xp >= cost_up:
                result.add(mastery)

        return result

    @property
    def attributes_count(self):
        return Masteries.achieved_level(self.xp_total) + 48

    @property
    def free_attribute_points(self):
        if self.preliminary_attributes:
            return self.attributes_count - sum(self.preliminary_attributes.values())
        else:
            return self.attributes_count - sum(self.base_type.attributes.values())

    @property
    def free_xp(self):
        if self.preliminary_masteries:
            return self.xp_total - self.preliminary_masteries.total_exp_spent
        else:
            return self.xp_total - self.masteries.total_exp_spent


    def increase_attrib(self, attrib_enum):
        if self.free_attribute_points <= 0:
            return

        assert attrib_enum in CharAttributes
        if self.preliminary_attributes is None :
            self.preliminary_attributes = copy.copy(self.base_type.attributes)
        self.preliminary_attributes[attrib_enum] += 1


    def increase_mastery(self, mastery):
        if not mastery in self.masteries_can_go_up:
            return

        if self.preliminary_masteries is None:
            self.preliminary_masteries = copy.copy(self.masteries)

        self.preliminary_masteries.level_up(mastery)


    def commit(self):
        self.base_type.attributes = self.preliminary_attributes
        self.preliminary_attributes = None

        self.masteries = self.preliminary_masteries
        self.preliminary_masteries = None


    def reset(self):
        self.preliminary_attributes = None
        self.preliminary_masteries = None

    @property
    def base_type_prelim(self):
        if not self.preliminary_attributes:
            return self.base_type
        else:
            cpy = copy.copy(self.base_type)
            cpy.attributes = self.preliminary_attributes
            return cpy


    @property
    def unit(self) -> Unit:
        return Unit(self.base_type_prelim)