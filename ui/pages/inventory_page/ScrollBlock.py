from __future__ import annotations

from PySide2.QtWidgets import QGraphicsSceneEvent, QGraphicsSceneMouseEvent
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages.AbstractPage import AbstractPage
    from ui.pages.suwidgets.BaseItem import BaseItem


class ScrollBlock:
    def __init__(self, page, width=0):
        """
        self.but -- scroll button
        self.but_left -- left border position
        self.but_right -- right border position
        self.width -- scroll bar width
        self.scroll_items -- scrolling items
        """
        self.page: AbstractPage = page
        self.but: BaseItem = None
        self.but_left, self.but_right = 0, 0
        self.width = width
        self.scroll_items = []
        self.items_width = 0
        self.items_step = 0
        self.delta_width = 0.
        self.isDown = False

    def addScrollItem(self, item: BaseItem):
        self.scroll_items.append(item)
        counts = len(self.scroll_items)
        if counts == 2:
            self.items_step = self.scroll_items[1]._left - self.scroll_items[0]._left
        item.scroll_x = item._left
        if counts > 1:
            self.items_width = counts * self.items_step
        self.delta_width = self.get_delta_width()
        self.item_set_visible(item)

    def _get_items_width(self):
        counts = len(self.scroll_items)
        if counts > 1:
            return self.scroll_items[counts-1]._left - self.scroll_items[0]._left + 2 * self.scroll_items[counts-1]._width
        elif counts == 1:
            return self.scroll_items[0]._width
        elif counts == 0:
            return 0

    def get_delta_width(self):
        if self.but is not None and len(self.scroll_items) > 1:
            return self.items_width - self.width - self.but.width
        else:
            return 0.

    def setScrollBut(self, but: BaseItem):
        self.but = but
        self.but_left = but._left
        self.but_right = self.but_left + self.width
        self.delta_width = self.get_delta_width()

    def get_pc(self) -> int:
        return (self.but_right - self.but._left) / self.width

    def scroll_but_move(self, event: QGraphicsSceneMouseEvent):
        x1 = event.pos().x() - self.but._left
        if event.pos().x() < self.but_left:
            x1 = self.but_left - self.but._left
        elif event.pos().x() > self.but_right:
            x1 = self.but_right - self.but._left
        self.but.move(x1, 0)

    def items_move(self):
        x2 = self.but_left - ((1. - self.get_pc()) * self.delta_width)
        l = len(self.scroll_items)
        for i in range(l):
            self.scroll_items[i].move(x2 + self.items_step * i - self.scroll_items[i]._left, 0)
            self.item_set_visible(self.scroll_items[i])

    def item_set_visible(self, item):
        if item._left < self.but_left or item._left > self.but_right:
            item.setVisible(False)
        else:
            item.setVisible(True)

    def is_scroll_but(self, event: QGraphicsSceneEvent):
        item = self.page.scene().itemAt(event.scenePos(), self.page.scene().views()[0].transform())
        return item.name == self.but.name

    def mousePressEvent(self, event:QGraphicsSceneEvent):
        if self.is_scroll_but(event):
            self.isDown = True

    def mouseReleaseEvent(self):
        self.isDown = False

    def mouseMoveEvent(self, event:QGraphicsSceneEvent):
        if self.isDown:
            self.scroll_but_move(event)
            self.items_move()
