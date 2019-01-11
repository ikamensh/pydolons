from PySide2 import QtCore, QtWidgets


class ToolTip(QtCore.QObject, QtWidgets.QGraphicsRectItem):
    """docstring for ToolTip.

    Размер тултипа автоматически подстраивается
    в методе setText(self, text)
    self.minimuWidth -- минимальная ширина тултипа, устанвливает в методе setFont()
    self.minimuWidth Зависит от шрифта и self.minimumLeters -- минимальное количество символов

    """
    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        QtWidgets.QGraphicsRectItem.__init__(self, parent)
        self.textItem = QtWidgets.QGraphicsTextItem()
        self.textItem.setParentItem(self)
        self.minimuWidth = 100
        self.minimumLeters = 16
        self.setZValue(10)


    def setDefaultTextColor(self, color):
        self.textItem.setDefaultTextColor(color)

    def setFont(self, font):
        self.textItem.setFont(font)
        tempText = self.textItem.toPlainText()
        self.textItem.setPlainText("#" * self.minimumLeters)
        self.minimuWidth = self.textItem.boundingRect().width()
        self.textItem.setPlainText(tempText)

    def setTextPos(self, x, y):
        self.textItem.setPos(x, y)

    def setText(self, text):
        self.textItem.setPlainText(text)
        h = self.textItem.boundingRect().height()
        self.setRect(self.textItem.x(), self.textItem.y(), self.minimuWidth, h)

    def setDict(self, data):
        result = ''
        for k, v in data.items():
            result = result + k + ' = ' + v + '\n'
        self.setText(result[:-1])
