from PySide2 import QtWidgets, QtCore, QtGui
from game_objects.items.on_unit.EquipmentSlotUids import EquipmentSlotUids


class SlotWidget(QtWidgets.QLabel):
    hovered = QtCore.Signal(QtCore.QObject)
    hover_out = QtCore.Signal(QtCore.QObject)
    slot_changed = QtCore.Signal(QtWidgets.QLabel, QtWidgets.QLabel)

    def __init__(self, *args, parent = None):
        super(SlotWidget, self).__init__(*args, parent=parent)
        self.name = None
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.start_point = QtCore.QPoint()
        self.dragStart = QtCore.QPoint()
        self.setAcceptDrops(True)
        self.setStyleSheet('background-color:rgba(127, 127, 127, 100);')
        self.isHover = False
        self.isDragLeave = True
        self.setAttribute(QtCore.Qt.WA_Hover)
        self.installEventFilter(self)

    def mousePressEvent(self, ev):
        self.dragStart = ev.pos()
        pass

    def mouseMoveEvent(self, ev):
        if ev.buttons() == QtCore.Qt.LeftButton:
            if QtWidgets.QApplication.startDragDistance() <= (ev.pos() - self.dragStart).manhattanLength():
                self.startDrag()

    def startDrag(self):
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        mimeData.setText(self.text())
        mimeData.setImageData(self.pixmap())
        # mimeData.setData('slot', self.property('slot'))
        drag.setMimeData(mimeData)
        result = drag.exec_(QtCore.Qt.CopyAction|QtCore.Qt.MoveAction)
        if result == QtCore.Qt.CopyAction or result == QtCore.Qt.MoveAction:
            self.slot_changed.emit(self, drag.target())
            self.clearSlot()

    def dragEnterEvent(self, ev:QtGui.QDragEnterEvent):
        formats = ev.mimeData().formats()
        if "text/plain" in formats:
            ev.setDropAction(QtCore.Qt.CopyAction)
            ev.setAccepted(True)
        if 'application/x-qt-image' in formats:
            ev.setDropAction(QtCore.Qt.CopyAction)
            ev.setAccepted(True)

    def dropEvent(self, ev:QtGui.QDropEvent):
        if ev.dropAction() != QtCore.Qt.IgnoreAction:
            self.setText(ev.mimeData().text())
            self.setPixmap(ev.mimeData().imageData())
            if self.name == EquipmentSlotUids.HANDS.name:
                self.property('hand').setText(ev.mimeData().text())
                self.property('hand').setPixmap(ev.mimeData().imageData())
            ev.acceptProposedAction()

    def eventFilter(self, watched:QtCore.QObject, event:QtCore.QEvent):
        if event.type() == QtCore.QEvent.HoverEnter:
            watched.hovered.emit(watched)
            self.isHover = True
            pass
        elif event.type() == QtCore.QEvent.HoverLeave:
            watched.hover_out.emit(watched)
            self.isHover = False
        elif event.type() == QtCore.QEvent.ContextMenu:
            self.showContextMenu(event.globalPos())
        return super(SlotWidget, self).eventFilter(watched, event)

    def showContextMenu(self, pos):
        print('showContextMenu pos', pos)

    def clearSlot(self):
        self.setText('empty')
        self.setPixmap(self.empty_pix)


