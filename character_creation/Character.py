import copy

from game_objects.battlefield_objects import BaseType, Unit
from game_objects.battlefield_objects.Unit import CharAttributes


class Character:
    def __init__(self, base_type : BaseType):
        self.base_type = base_type
        self.free_xp = 500
        self.attributes_points = 10

        self.preliminary_points = []

    def increase_attrib(self, attrib_enum):
        assert attrib_enum in CharAttributes
        if self.attributes_points > 0 :
            self.preliminary_points.append(attrib_enum)
            self.preliminary_points -= 1


    def commit(self):
        self.base_type = self.base_type_prelim
        self.preliminary_points = []

    def reset(self):
        self.attributes_points += len(self.preliminary_points)
        self.preliminary_points = []

    @property
    def base_type_prelim(self):
        attribs = self.base_type.attributes
        for point in self.preliminary_points:
            attribs[point] += 1
        cpy = copy.deepcopy(self.base_type)
        cpy.attributes = attribs
        return cpy


    @property
    def unit(self) -> Unit:
        return Unit(self.base_type_prelim)