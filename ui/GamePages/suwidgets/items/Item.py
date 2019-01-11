from ui.gamecore import GameObject
from PySide2 import QtWidgets, QtCore


class Item(GameObject):

    def __init__(self, *args,page, parent = None):
        super(Item, self).__init__(*args, parent)
        self.page = page
        self.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.mouse_pos = QtCore.QPoint()
        self.setZValue(100)
        self.hide()

    def setMousePos(self, x, y):
        self.mouse_pos.setX(x)
        self.mouse_pos.setY(y)
        self.setPos(self.page.gamePages.gameRoot.view.mapToScene(self.mouse_pos.x(), self.mouse_pos.y()))

    def setSlot(self, slot):
        self.setPixmap(slot.pixmap())
        self.show()

    def removeSlot(self):
        self.hide()

    def resized(self):
        self.setPos(self.page.gamePages.gameRoot.view.mapToScene(self.mouse_pos.x(), self.mouse_pos.y()))
