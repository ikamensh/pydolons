import copy

from game_objects.battlefield_objects import BaseType, Unit, CharAttributes
from character_creation.Masteries import Masteries, MasteriesEnum


class Character:
    def __init__(self, base_type : BaseType):
        self.base_type = base_type
        self.masteries = Masteries()
        self.xp = base_type.xp


        self.temp_attributes = None
        self.temp_masteries = None

    @property
    def masteries_can_go_up(self):
        result = set()

        mastery_map = self.temp_masteries or self.masteries

        for mastery in MasteriesEnum:
            cost_up, *_ = mastery_map.calculate_cost(mastery)
            if self.free_xp >= cost_up:
                result.add(mastery)

        return result

    @property
    def attributes_count(self):
        return Masteries.achieved_level(self.xp) + 48

    @property
    def free_attribute_points(self):
        if self.temp_attributes:
            return self.attributes_count - sum(self.temp_attributes.values())
        else:
            return self.attributes_count - sum(self.base_type.attributes.values())

    @property
    def free_xp(self):
        if self.temp_masteries:
            return self.xp - self.temp_masteries.total_exp_spent
        else:
            return self.xp - self.masteries.total_exp_spent


    def increase_attrib(self, attrib_enum):
        if self.free_attribute_points <= 0:
            return

        assert attrib_enum in CharAttributes
        if self.temp_attributes is None :
            self.temp_attributes = copy.copy(self.base_type.attributes)
        self.temp_attributes[attrib_enum] += 1


    def increase_mastery(self, mastery):
        if not mastery in self.masteries_can_go_up:
            return

        if self.temp_masteries is None:
            self.temp_masteries = copy.copy(self.masteries)

        self.temp_masteries.level_up(mastery)


    def commit(self):
        self.base_type.attributes = self.temp_attributes
        self.temp_attributes = None

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
        return Unit(self.base_type_prelim, masteries=self.temp_masteries or self.masteries)


    def update(self, unit : Unit):
        self.xp = unit.xp