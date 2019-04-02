from __future__ import annotations

from PySide2.QtWidgets import QGraphicsObject, QStyleOptionGraphicsItem, QWidget
from PySide2.QtGui import QPainter, QBrush
from PySide2 import QtCore
from battlefield.Cell import Cell
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.gamecore.GameRootNode import GameRootNode
    from PySide2.QtGui import QPixmap


class TileItem(QGraphicsObject):
    def __init__(self, gameRoot, parent=None, w =1, h=1):
        super(TileItem, self).__init__(parent)
        self.gameRoot: GameRootNode = gameRoot
        self.pixmaps = {}
        self._brushs = {}
        self.cells = {}
        self._positions = {}
        self._width = w
        self._height = h
        self._cell_1: Cell = None
        self._cell_2: Cell = None
        pass

    def add_pixmap(self, id:int, pixmap:QPixmap):
        self.pixmaps[id] = pixmap
        self._brushs[id] = QBrush(pixmap)
        pass

    def add_cell(self, id:int, cell:Cell):
        self.cells[cell] = id
        self._positions[(cell.x * self._width, cell.y * self._height)] = id
        self.__calculate_bound(cell)
        if self.gameRoot is not None:
            if not self.is_id(id):
                self.add_pixmap(id, self.gameRoot.cfg.getPicFile(''))

    def is_pixmap(self, pixmap:QPixmap)->bool:
        return pixmap in self.pixmaps.values()

    def is_cell(self, cell:Cell)->bool:
        return cell in self.cells.values()

    def is_id(self, id)->bool:
        return id in self.pixmaps.keys()

    def __calculate_bound(self, cell: Cell):
        self.boundingRect = self._boundingRect
        if self._cell_1 is None:
            self._cell_1 = Cell(cell.x, cell.y)
            self._cell_2 = Cell(cell.x, cell.y)
        else:
            if cell.x < self._cell_1.x:
                self._cell_1.x = cell.x
            if cell.y < self._cell_1.y:
                self._cell_1.y = cell.y
            if cell.x > self._cell_2.x:
                self._cell_2.x = cell.x
            if cell.y > self._cell_2.y:
                self._cell_2.y = cell.y

    def paint(self,  painter:QPainter, option:QStyleOptionGraphicsItem, widget:QWidget=...):
        for pos, id in self._positions.items():
            painter.drawPixmap(pos[0], pos[1], self._width, self._height, self.pixmaps[id])

    def boundingRect(self):
        return QtCore.QRectF(self.pos().x(),
                            self.pos().y(),
                            0, 0)

    def _boundingRect(self)-> QtCore.QRectF:
        return QtCore.QRectF(self.pos().x(),
                            self.pos().y(),
                            self.pos().x() + self._cell_2.x * self._width,
                            self.pos().y() + self._cell_2.y * self._height)

    def rect(self)-> QtCore.QRectF:
        return self.boundingRect()

