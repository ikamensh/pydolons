from PySide2.QtCore import QPointF, QEvent
from PySide2.QtWidgets import QGraphicsSceneEvent


class ScrollBlock:
    def __init__(self, page, width=0):
        self.page = page
        self.but = None
        self.but_step = 0
        self.start_pos = QPointF(0., 0.)
        self.delta_x = 0.
        self.delta_y = 0.
        self.width = width
        self.items_width = 0
        self.items_step = 0
        self.scoll_items = []
        self.isDown = False
        pass

    def addScrollItem(self, item):
        self.scoll_items.append(item)
        item.scroll_x = item._left
        self.items_width = self.getItemsWidth()
        self.items_step = (self.items_width - self.width) / 100
        self.item_set_visible(item)

    def getItemsWidth(self):
        l = len(self.scoll_items)
        if l > 1:
            return self.scoll_items[l - 1]._left - \
                self.scoll_items[0]._left + 2 * self.scoll_items[l - 1]._width
        elif l == 1:
            return self.scoll_items[0]._width
        elif l == 0:
            return 0

    def setScrollBut(self, but):
        self.but = but
        self.but_x = but._left
        self.but_left = but._left
        self.but_right = self.width
        self.but_step = self.width / 100

    def but_move(self):
        x = self.but_x - self.delta_x
        if x >= self.but_left and x <= self.but_right:
            self.but._left = x
            self.items_move()
        elif x < self.but_left:
            self.but._left = self.but_left
        elif x > self.but_right:
            self.but._left = self.but_right

    def items_move(self):
        for item in self.scoll_items:
            item._left = item.scroll_x + self.items_step * self.getValue()
            self.item_set_visible(item)

    def item_set_visible(self, item):
        if item._left < self.but_left or item._left > self.but_right:
            item.setVisible(False)
        else:
            item.setVisible(True)

    def items_upate_pos(self):
        for item in self.scoll_items:
            item.scroll_x = item.scroll_x + self.items_step * self.getValue()

    def isScrollBut(self, event: QGraphicsSceneEvent):
        item = self.page.scene().itemAt(
            event.scenePos(),
            self.page.scene().views()[0].transform())
        return item.name == self.but.name

    def mousePressEvent(self, event: QGraphicsSceneEvent):
        if self.isScrollBut(event):
            self.start_pos.setX(event.screenPos().x())
            self.start_pos.setY(event.screenPos().y())
            self.isDown = True

    def mouseReleaseEvent(self):
        self.isDown = False
        x = self.but_x - self.delta_x
        if x >= self.but_left and x <= self.but_right:
            self.but_x = x
            self.items_upate_pos()

    def mouseMoveEvent(self, event: QGraphicsSceneEvent):
        if self.isDown:
            self.delta_x = self.start_pos.x() - event.screenPos().x()
            self.delta_y = self.start_pos.y() - event.screenPos().y()
            self.but_move()

    def getValue(self):
        return int(self.delta_x / self.but_step)
