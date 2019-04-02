from PySide2 import QtCore, QtWidgets

class SelectItem(QtWidgets.QGraphicsRectItem):

    def __init__(self, *arg):
        super(SelectItem, self).__init__(*arg)
        self.setBrush(QtCore.Qt.cyan)
        self.setOpacity(0.3)