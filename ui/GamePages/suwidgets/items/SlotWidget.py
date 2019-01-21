from PySide2 import QtWidgets, QtCore, QtGui
from ui.GamePages.suwidgets.items.GropsTypes import GropusTypes
from game_objects.items.on_unit.EquipmentSlotUids import EquipmentSlotUids


class SlotWidget(QtWidgets.QGraphicsObject, QtWidgets.QGraphicsLayoutItem):
    hovered = QtCore.Signal(QtCore.QObject)
    hover_out = QtCore.Signal(QtCore.QObject)
    slot_changed = QtCore.Signal(QtWidgets.QLabel, QtWidgets.QLabel)

    def __init__(self, name,  page, slot_type, parent = None):
        QtWidgets.QGraphicsObject.__init__(self, parent)
        QtWidgets.QGraphicsLayoutItem.__init__(self, parent)
        self.page = page
        self.cfg = page.gamePages.gameRoot.cfg
        self.name = name
        self.slot_type = slot_type
        self.installSceneEventFilter(self)
        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton|QtCore.Qt.RightButton)
        self._pos = QtCore.QPoint(-10, -10)
        self.brush = self.cfg.brushs['b5adb7']
        self.pen = QtGui.QPen()
        self.pen.setBrush(QtCore.Qt.NoBrush)
        self._drag = False
        self.isHover = False
        self.isDown = False
        self.isChecked = False
        self.simple_drag = False
        self.installEventFilter(self)
        self.state = False

    def setPixmap(self, pixmap:QtGui.QPixmap):
        if pixmap is not None:
            self._geometry = QtCore.QRectF(self.pos().x(), self.pos().y(), pixmap.height(), pixmap.height())
        self._pixmap = pixmap

    def pixmap(self):
        return self._pixmap

    def boundingRect(self):
        return QtCore.QRect(0, 0, self._geometry.width(), self._geometry.height())

    def paint(self, painter:QtGui.QPainter, option:QtWidgets.QStyleOptionGraphicsItem, widget:QtWidgets.QWidget=...):
        painter.setPen( self.pen)
        painter.setBrush(self.brush)
        painter.setBackground(self.brush)
        painter.drawRect(0, 0, self._geometry.width(), self._geometry.height())
        if self._pixmap is not None:
            painter.drawPixmap(0, 0, self._pixmap)

    def sizeHint(self, which:QtCore.Qt.SizeHint = None, constraint:QtCore.QSizeF=None):
        return QtCore.QSize(self.boundingRect().width(), self.boundingRect().height())

    def geometry(self):
        return QtCore.QRectF(0, 0, 64, 64)

    def sceneEventFilter(self, watched:QtWidgets.QGraphicsItem, event:QtCore.QEvent):
        return True

    def mouseReleaseEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent):
        if self.isDown:
            if self.isChecked:
                self.isChecked = False
                self.brush = self.cfg.brushs['b5adb7']
            else:
                self.isChecked = True
                self.brush = self.cfg.brushs['d7a784']
            self.page.startManipulation(self)
            self.isDown = False
        self.setZValue(0.0)
        self.update(0, 0, self._geometry.width(), self._geometry.height())

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        self.dragStart = event.pos()
        if event.buttons() == QtCore.Qt.LeftButton:
            self.isDown = True
        elif event.buttons() == QtCore.Qt.RightButton:
            self.pressRighBtn()
        self._pos = event.pos()

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        if event.buttons() == QtCore.Qt.LeftButton:
            if QtWidgets.QApplication.startDragDistance() <= (event.pos() - self.dragStart).manhattanLength():
                self.startDrag()
        pass

    def moveToMouse(self, event):
        if self._drag:
            pos = self.scene().views()[0].mapToScene(event.pos())
            # self.setPos(pos)
            self.setX(pos.x() - self._pos.x())
            self.setY(pos.y() - self._pos.y())
        pass

    def hoverEnterEvent(self, event:QtWidgets.QGraphicsSceneHoverEvent):
        self.brush = self.cfg.brushs['d7a784']
        self.hovered.emit(self)
        self.update(0, 0, self._geometry.width(), self._geometry.height())

    def hoverLeaveEvent(self, event:QtWidgets.QGraphicsSceneHoverEvent):
        if not self.isChecked:
            self.brush = self.cfg.brushs['b5adb7']
        self.hover_out.emit(self)
        self.update(0, 0, self._geometry.width(), self._geometry.height())

    def dragEnterEvent(self, ev:QtGui.QDragEnterEvent):
        formats = ev.mimeData().formats()
        self.brush = self.cfg.brushs['d7a784']
        self.update(0, 0, self._geometry.width(), self._geometry.height())
        if "text/plain" in formats:
            ev.setDropAction(QtCore.Qt.CopyAction)
            ev.setAccepted(True)
            ev.acceptProposedAction()

    def dropEvent(self, ev:QtGui.QDropEvent):
        # Step 1
        if ev.dropAction() != QtCore.Qt.IgnoreAction:
            self.page.startManipulation(self)
            ev.acceptProposedAction()
        pass

    def dragLeaveEvent(self, event:QtWidgets.QGraphicsSceneDragDropEvent):
        self.brush = self.cfg.brushs['b5adb7']
        self.update(0, 0, self._geometry.width(), self._geometry.height())
        pass

    def startDrag(self):
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        mimeData.setText(self.name)
        drag.setPixmap(self.pixmap())
        drag.setMimeData(mimeData)
        result = drag.exec_(QtCore.Qt.CopyAction|QtCore.Qt.MoveAction)
        self.page.startManipulation(self)
        if result == QtCore.Qt.IgnoreAction:
            self.page.drop(self.property('slot'))

    def pressRighBtn(self):
        if self.slot_type == GropusTypes.INVENTORY:
            self.page.equip(self)
        elif self.slot_type == GropusTypes.EQUIPMENT:
            self.page.unequip_slot(self)
        elif self.slot_type == GropusTypes.SHOP:
            print('Buy man!')
            self.page.buy(self)
        pass

    def setDefaultStyle(self):
        self.brush = self.cfg.brushs['b5adb7']
        self.isChecked = False
        self.isDown = False
        self.update(0, 0, self._geometry.width(), self._geometry.height())

    def update_slot(self):
        self.setPicSlot(self.property('slot'))

    def setPicSlot(self, game_slot):
        pixmap = self.cfg.getPicFile('slot.png', 101005001)
        self.empty_pix = pixmap
        if game_slot.content is not None:
            pixmap = self.cfg.getPicFile(game_slot.content.icon, 101005001)
        self.setPixmap(pixmap)

    def setData(self, mimeData, target):
        target.setPixmap(mimeData.imageData())
        if target.name == EquipmentSlotUids.HANDS.name:
            target.property('hand').setPixmap(mimeData.imageData())

    def clearSlot(self):
        self.setPixmap(self.empty_pix)



