from __future__ import annotations
from game_objects import items
from my_utils.utils import tractable_value
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.items.materials.MaterialTypes import MaterialTypes


class MaterialPieces(items.Item):
    def __init__(self, material, pieces):
        super().__init__(material.name, items.ItemTypes.MATERIAL)
        self.pieces = pieces


class Material:
    BASE_PRICE = 30

    def __init__(
            self,
            material_type: MaterialTypes,
            name,
            rarity,
            magic_complexity=1,
            energy=50):
        self.material_type = material_type
        self.name = name
        self.rarity = rarity
        self.magic_complexity = magic_complexity
        self.energy = energy

        self.value = self.rarity ** 2.7 * \
            (1 + (self.magic_complexity - 1) ** 2 + (self.energy - 50) / 150)

    @property
    def price(self):
        return tractable_value(
            Material.BASE_PRICE * (1e-3 * self.value**5 + 1e-2 * self.value**3 + self.value))

    def to_pieces(self, count_pieces):
        return MaterialPieces(self, count_pieces)

    def __repr__(self):
        return f"{self.name}"
