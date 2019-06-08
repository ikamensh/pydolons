from __future__ import annotations

from PySide2 import QtCore, QtGui, QtWidgets

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages import AbstractPage


class UnitsStack(QtWidgets.QGraphicsItem):
    def __init__(self, page):
        super(UnitsStack, self).__init__()
        self.page: AbstractPage = page
        self.units = {}
        self.pic_units = {}

        # setUp step
        self.step = int((64 * self.page.gamePages.gameRoot.cfg.scale_x) + 0.5)
        # self.half_step = self.step/2

        self.timeLine = QtCore.QTimeLine(1000, None)
        self.timeLine.setFrameRange(0, 100)
        self.timeLine.frameChanged.connect(self.setVal)
        self.timeLine.finished.connect(self.finish_anim)
        # self.timeLine.start()

        self.v = 0
        self.uid = -1

        self.state = True

    def setVal(self, i):
        """
        :param i:
        :return:
        slef.v this value to change beginer position y, y = y + slef.v-> y = 100+1, ... y = 100+100
        """
        self.v = i
        self.update()

    def paint(self, painter:QtGui.QPainter, option:QtWidgets.QStyleOptionGraphicsItem, widget:QtWidgets.QWidget=...):
        painter.setBrush(QtCore.Qt.green)
        x = 0
        for unit in self.units:
            if unit.uid != self.uid:
                painter.setOpacity(1.0)
                painter.drawPixmap(x * self.step, self.y(), self.step, self.step, self.pic_units[unit.uid])
                # painter.drawRect(x * self.step + 4, self.y(), self.step, self.step)
                # painter.drawText(x * self.step + 4 + self.half_step, self.y() + self.half_step, str(unit.uid))
            else:
                painter.setOpacity(1 - self.v/100)
                painter.drawPixmap(x * self.step, self.y()+self.v,self.step, self.step, self.pic_units[unit.uid])
                # painter.drawRect(x * self.step + 4, self.y() +self.v, self.step, self.step)
                # painter.drawText(x * self.step + 4 + self.half_step, self.y() + self.half_step+self.v, str(unit.uid))
            x += 1

    def boundingRect(self):
        return QtCore.QRectF(self.x(), self.y(), self.step * (len(self.units) + 2), self.step << 2)

    def finish_anim(self):
        del self.pic_units[self.uid]
        for i in range(len(self.units)):
            if self.units[i].uid == self.uid:
                self.units.pop(i)
                break
        self.state = True

    def remove_unit(self, uid):
        self.uid = uid
        self.state = False
        self.timeLine.start()

    def update_stack(self, units):
        if self.state:
            self.units = units
            for unit in units:
                self.pic_units[unit.uid] = self.page.gamePages.gameRoot.cfg.getPicFile(unit.icon)
            self.update()


