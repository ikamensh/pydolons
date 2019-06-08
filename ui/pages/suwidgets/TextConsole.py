from PySide2 import QtCore, QtGui, QtWidgets
import textwrap


class TextCosole(QtWidgets.QGraphicsItem):
    def __init__(self, log):
        super(TextCosole, self).__init__()
        self.log = log
        self.text_stack = []
        self.last_msg = ''

        # self.timeLine = QtCore.QTimeLine(500, None)
        # self.timeLine.setFrameRange(0, 100)
        # # self.timeLine.frameChanged.connect(self.setVal)
        # self.timeLine.finished.connect(self.finish_anim)
        # # self.timeLine.start()
        # self.v = 0

        self.wrapper = textwrap.TextWrapper(width=45)

        self.pens = {'R':QtGui.QPen(),'G':QtGui.QPen(), 'B':QtGui.QPen()}
        self.pens['R'].setColor(QtCore.Qt.red)
        self.pens['G'].setColor(QtCore.Qt.green)
        self.pens['B'].setColor(QtCore.Qt.white)

    # def setVal(self, i):
    #     self.v = i
    #
    # def finish_anim(self):
    #     pass

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: QtWidgets.QWidget = ...):
        y = 0
        for s in self.text_stack:
            painter.setPen(self.pens['G'])
            painter.drawText(self.x(), self.y() + y, s)
            y += 22

    def game_event(self, event):
        if self.last_msg != event:
            self.last_msg = event
            for s_m in self.wrapper.wrap(str(self.last_msg)):
                if len(self.text_stack) > 10:
                    self.text_stack.pop(0)
                self.text_stack.append(s_m)
        self.update()

    def boundingRect(self):
        return QtCore.QRectF(self.x(), self.y() - 64, 512, 512)



