from __future__ import annotations

from PySide2 import QtCore, QtWidgets
from ui.world.TileItem import TileItem
from battlefield.Cell import Cell

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.core.gameconfig.GameConfiguration import GameConfiguration
    from battlefield.Battlefield import Battlefield
    from game_objects.battlefield_objects import Wall
    from ui.core.levels.BaseLevel import BaseLevel
    from PySide2.QtGui import QPixmap
    from typing import Dict


class GameWorld(QtWidgets.QGraphicsItemGroup):
    def __init__(self, cfg):
        super().__init__()
        self.cfg: GameConfiguration = cfg
        self.size = QtCore.QRectF(0., 0., 1., 1.)
        self.worldSize = (1, 1)
        self.worldHalfSize = (1, 1)
        self.level: BaseLevel = None
        self.floor: TileItem = None
        self.obstacles = {}

    def setLevel(self, level):
        self.level = level
        self.level.world = self

    def setWorldSize(self, w, h):
        self.worldSize = (w, h)
        self.worldHalfSize = (int(w / 2), int(h / 2))
        self.size.setWidth(self.cfg.unit_size[0] * w)
        self.size.setHeight(self.cfg.unit_size[1] * h)
        # x = (self.cfg.dev_size[0] - self.size.width()) / 2
        # y = (self.cfg.dev_size[1] - self.size.height()) / 2
        # # self.setPos(x, y)

    def setFloor(self, pixMap: QPixmap):
        self.floor = TileItem(gameRoot=self.cfg.gameRoot, w=pixMap.width(), h=pixMap.width())
        self.floor.add_pixmap(0, pixMap)
        for i in range(self.worldSize[0]):
            for j in range(self.worldSize[1]):
                self.floor.add_cell(0, Cell(i, j))
        self.addToGroup(self.floor)

    def setWall(self, walls: Dict[Cell, Wall]):
        for cell, wall in walls.items():
            pixmap = self.cfg.getPicFile(wall.icon, 102001001)
            if not self.floor.is_pixmap(pixmap):
                self.floor.add_pixmap(wall.icon, pixmap)
            self.floor.add_cell(wall.icon, cell)

    def setUpFloors(self, bf: Battlefield):
        self.setFloor(self.cfg.getPicFile('floor.png', 102001001))
        if bf.walls is not {}:
            self.setWall(bf.walls)

