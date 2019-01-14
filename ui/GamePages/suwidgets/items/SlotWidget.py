from PySide2 import QtWidgets, QtCore, QtGui
from game_objects.items.on_unit.EquipmentSlotUids import EquipmentSlotUids
from ui.GamePages.suwidgets.items.GropsTypes import GropusTypes


class SlotWidget(QtWidgets.QLabel):
    hovered = QtCore.Signal(QtCore.QObject)
    hover_out = QtCore.Signal(QtCore.QObject)
    slot_changed = QtCore.Signal(QtWidgets.QLabel, QtWidgets.QLabel)

    def __init__(self, *args, page, type, parent = None):
        super(SlotWidget, self).__init__(*args, parent=parent)
        self.page = page
        self.cfg  = page.gamePages.gameRoot.cfg
        self.name = None
        self.type = type
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.start_point = QtCore.QPoint()
        self.dragStart = QtCore.QPoint()
        self.setAcceptDrops(True)
        # self.setDefaultStyle()
        self.isHover = False
        self.isDown = False
        self.isChecked = False
        self.simple_drag = False
        self.setAttribute(QtCore.Qt.WA_Hover)
        self.installEventFilter(self)
        self.state = False
        self.setToolTip('this slot')

    def setUpStyle(self):
        pic_path = self.cfg.pic_file_paths.get('active_select_96.png')
        # self.setStyleSheet('background-color:rgba(127, 127, 127, 100);')
        # print(pic_path)
        res = ''
        res = 'border: 10px solid #40c4c8;'
        res += 'border-image: url('+pic_path+') 10 round round;'
        self.setStyleSheet(res)

    def setDefaultStyle(self):
        self.setStyleSheet('background-color:rgba(127, 127, 127, 100);')

    def mousePressEvent(self, event):
        self.dragStart = event.pos()
        if event.buttons() == QtCore.Qt.RightButton:
            self.pressRighBtn()
        elif event.buttons() == QtCore.Qt.LeftButton:
            self.isDown = True

    def mouseReleaseEvent(self, ev:QtGui.QMouseEvent):
        if self.isDown:
            if self.isChecked:
                self.isChecked = False
                self.setDefaultStyle()
            else:
                self.isChecked = True
                self.setUpStyle()
            self.page.startManipulation(self)
            self.isDown = False

    def mouseMoveEvent(self, ev):
        if ev.buttons() == QtCore.Qt.LeftButton:
            if QtWidgets.QApplication.startDragDistance() <= (ev.pos() - self.dragStart).manhattanLength():
                self.startDrag()

    def startDrag(self):
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        mimeData.setText(self.text())
        mimeData.setImageData(self.pixmap())
        drag.setPixmap(self.pixmap())
        # mimeData.setData('slot', self.property('slot'))
        drag.setMimeData(mimeData)
        # result = drag.exec_(QtCore.Qt.CopyAction|QtCore.Qt.MoveAction)
        result = drag.exec_()
        if drag.target() == self:
            return
        if self.property('slot').content is None:
            return
        if result == QtCore.Qt.CopyAction or result == QtCore.Qt.MoveAction:
            # Step 2
            self.state = self.page.swap_item(self, drag.target())
            if self.state:
                self.setData(mimeData, drag.target())
                self.clearSlot()
        elif result == QtCore.Qt.IgnoreAction:
            self.page.drop(self.property('slot'))

    def dragEnterEvent(self, ev:QtGui.QDragEnterEvent):
        formats = ev.mimeData().formats()
        if "text/plain" in formats:
            ev.setDropAction(QtCore.Qt.CopyAction)
            ev.setAccepted(True)
        if 'application/x-qt-image' in formats:
            ev.setDropAction(QtCore.Qt.CopyAction)
            ev.setAccepted(True)

    def dropEvent(self, ev:QtGui.QDropEvent):
        # Step 1
        if ev.dropAction() != QtCore.Qt.IgnoreAction:
            ev.acceptProposedAction()
        pass

    def setData(self, mimeData, target):
        target.setText(mimeData.text())
        target.setPixmap(mimeData.imageData())
        if target.name == EquipmentSlotUids.HANDS.name:
            target.property('hand').setText(mimeData.text())
            target.property('hand').setPixmap(mimeData.imageData())

    def eventFilter(self, watched:QtCore.QObject, event:QtCore.QEvent):
        # if event.type() == QtCore.QEvent.ToolTip:
        #     print('tool tip')
        if event.type() == QtCore.QEvent.HoverEnter:
            watched.hovered.emit(watched)
            self.isHover = True
        elif event.type() == QtCore.QEvent.HoverLeave:
            watched.hover_out.emit(watched)
            self.isHover = False
        return super(SlotWidget, self).eventFilter(watched, event)

    def showContextMenu(self, pos):
        print('showContextMenu pos', pos)

    def clearSlot(self):
        self.setText('empty')
        self.setPixmap(self.empty_pix)

    def pressRighBtn(self):
        if self.type == GropusTypes.INVENTORY:
            self.page.equip(self.property('slot'))

    def pressLeftBtn(self):
        print('Press left btn')
        pass


