from __future__ import annotations
from game_objects.battlefield_objects import Obstacle
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit

class Corpse(Obstacle):
    size = 1

    def __init__(self, unit: Unit):
        assert not unit.alive
        self.unit = unit
        self.unit.corpse = self
        super().__init__(name=f"Dead {unit.type_name}",
                         cell=unit.cell,
                         game=unit.game,
                         max_health=unit.max_health * 10,
                         armor=unit.armor,
                         resists=unit.resists,
                         icon='corpse.jpg')
