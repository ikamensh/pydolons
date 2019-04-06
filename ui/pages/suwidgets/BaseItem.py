from __future__ import annotations

from PySide2.QtWidgets import QGraphicsObject, QStyleOptionGraphicsItem, QWidget
from PySide2.QtGui import QPainter, QColor, QBrush, QPixmap
from PySide2 import QtCore

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages import AbstractPage
    from ui.core.GameRootNode import GameRootNode
    from ui.core.gameconfig.GameConfiguration import GameConfiguration


class BaseItem(QGraphicsObject):
    def __init__(self, page, parent=None):
        super().__init__(parent)
        self.gameRoot: GameRootNode = page.gamePages.gameRoot
        self.page: AbstractPage = page
        self.attrib: dict = None
        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton | QtCore.Qt.RightButton)
        self.isHover = False
        self.isDown = False
        self.isChecked = False
        self.cfg: GameConfiguration = page.gamePages.gameRoot.cfg
        self.scale_x = self.gameRoot.cfg.scale_x
        self.scale_y = self.gameRoot.cfg.scale_y
        self.scale_x = self.scale_y
        self.pixmap: QPixmap = None
        self._bg_brush: QBrush = None

    def setUpAttrib(self, attrib):
        self.attrib = attrib
        self.checkAttrib(attrib)
        self.name = attrib['name']
        self._names = attrib['name'].split('_')
        self._top = int(attrib.get('top')) * self.scale_x
        self._left = int(attrib.get('left')) * self.scale_x
        self._width = int(attrib.get('width')) * self.scale_x
        self._height = int(attrib.get('height')) * self.scale_x
        if attrib.get('position') is not None:
            self._position = attrib.get('position')
            if self._position == 'inherit':
                if self._parent_node is not None:
                    self._top = self.page.items[self._parent_node]._top + self._top
                    self._left = self.page.items[self._parent_node]._left + self._left

    def checkAttrib(self, attrib):
        if attrib.get('width') is None:
            attrib['width'] = '0'
        if attrib.get('height') is None:
            attrib['height'] = '0'
        if attrib.get('top') is None:
            attrib['top'] = 1080 - int(attrib['bottom'])
        if attrib.get('left') is None:
            attrib['left'] = 1920 - int(attrib['right'])
        self._parent_node = attrib.get('parent_node')
        if attrib.get('background-color') is not None:
            self._bg_brush = QBrush(QColor(attrib['background-color']))
        if attrib.get('icon') is not None:
            self.pixmap = self.gameRoot.cfg.getPicFile(attrib['icon'])
        if attrib.get('background-color') is not None:
            self.paint = self.paint_bg
        if attrib.get('icon') is not None:
            self.paint = self.paint_pic
        if attrib.get('icon') is not None and attrib.get('background-color') is not None:
            self.paint = self.paint_pic_bg
        if attrib.get('input') is None:
            self.input = ''
        else:
            self.input = attrib.get('input')

    def boundingRect(self):
        return QtCore.QRect(self._left, self._top, self._width, self._height)

    def paint(self, painter:QPainter, option:QStyleOptionGraphicsItem, widget:QWidget=...):
        painter.drawRect(self._left, self._top, self._width, self._height)

    def paint_bg(self, painter:QPainter, option:QStyleOptionGraphicsItem, widget:QWidget=...):
        painter.setBrush(self._bg_brush)
        painter.drawRect(self._left, self._top, self._width, self._height)

    def paint_pic(self, painter:QPainter, option:QStyleOptionGraphicsItem, widget:QWidget=...):
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.drawPixmap(self._left, self._top, self._width, self._height, self.pixmap)

    def paint_pic_bg(self, painter:QPainter, option:QStyleOptionGraphicsItem, widget:QWidget=...):
        painter.setBrush(self._bg_brush)
        painter.drawRect(self._left, self._top, self._width, self._height)
        painter.drawPixmap(self._left, self._top, self._width, self._height, self.pixmap)

    @property
    def width(self):
        return int(self.attrib.get('width')) * self.scale_x

    def update(self):
        super(BaseItem, self).update(self._left, self._top, self.width, self._height)

    def setPixmapIcon(self, icon:str):
        self.pixmap = self.gameRoot.cfg.getPicFile(icon)










