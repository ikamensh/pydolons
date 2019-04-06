from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.core.GameRootNode import GameRootNode
    from ui.world.units import Units
    from ui.world.units import UnitMiddleLayer
    from ui.world import GameWorld


class BaseLevel:
    def __init__(self):
        super().__init__()
        self.gameRoot: GameRootNode = None
        self.middleLayer: UnitMiddleLayer = None
        self.world: GameWorld = None
        self.units: Units = None

    def setGameRoot(self, gameRoot: GameRootNode):
        self.gameRoot = gameRoot
        self.gameRoot.level = self

    def setMiddleLayer(self, middleLayer: UnitMiddleLayer):
        self.middleLayer = middleLayer
        self.middleLayer.level =  self

    def setGameWorld(self, world: GameWorld):
        self.world = world
        self.world.level = self

    def setUnits(self, units: Units):
        self.units = units
        self.units.level = self

    def setStatus(self, status):
        self.gameRoot.gamePages.gameMenu.showNotify(status)
