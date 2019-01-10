from PySide2 import QtCore, QtWidgets, QtGui


class ItemTest(QtWidgets.QGraphicsRectItem):

    def __init__(self, page):
        super(ItemTest, self).__init__()
        self.page = page
        self.setBrush(QtCore.Qt.red)
        self.setRect(0, 0, 64, 64)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)

    def sceneEvent(self, event:QtCore.QEvent):
        # event.setAccepted(True)
        # print('accept', event.isAccepted())
        # print(event)
        # # print('ignore', event.ignore())
        if isinstance(event, QtWidgets.QGraphicsSceneMouseEvent):
            if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
                self.mousePressEvent(event)
                print(event)
        return super(ItemTest, self).sceneEvent(event)

    def sceneEventFilter(self, watched:QtWidgets.QGraphicsItem, event:QtCore.QEvent):
        print(event)
        return super(ItemTest, self).sceneEventFilter(watched, event)

    def mousePressEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent):
        super(ItemTest, self).mousePressEvent(event)
        print('press btn')
        pass

    def mouseMoveEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent):
        super(ItemTest, self).mouseMoveEvent(event)
        print(event.pos())
        pass
