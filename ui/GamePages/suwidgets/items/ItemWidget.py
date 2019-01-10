from PySide2 import QtCore, QtWidgets, QtGui


class ItemWidget(QtWidgets.QLabel):
    hovered = QtCore.Signal(QtCore.QObject)
    hover_out = QtCore.Signal(QtCore.QObject)

    def __init__(self, *args, parent = None):
        super(ItemWidget, self).__init__(*args, parent)
        self.setAcceptDrops(True)
        self.setAttribute(QtCore.Qt.WA_Hover)
        self.installEventFilter(self)
        self.setStyleSheet('background-color:rgba(127, 127, 127, 100);')

    def eventFilter(self, watched:QtCore.QObject, event:QtCore.QEvent):
        if event.type() == QtCore.QEvent.HoverEnter:
            watched.hovered.emit(watched)
            pass
        elif event.type() == QtCore.QEvent.HoverLeave:
            watched.hover_out.emit(watched)
        elif event.type() == QtCore.QEvent.DragEnter:
            print('DragEnter')
        # elif event.type() == QtCore.QEvent.DragMove:
        #     print('DragMove')
        elif event.type() == QtCore.QEvent.Drop:
            print('Drop')
        return QtWidgets.QWidget.eventFilter(self, watched, event)

    def mouseMoveEvent(self, ev):
        if ev.buttons() == QtCore.Qt.LeftButton:
            self.move(ev.pos())

    def dragEnterEvent(self, ev:QtGui.QDragEnterEvent):
        formats = ev.mimeData().formats()

        if "text/plain" in formats:
            print('formats', formats)
            ev.acceptProposedAction()
        ev.accept()

    def dropEvent(self, ev:QtGui.QDropEvent):
        self.setText(ev.mimeData().text())
        ev.acceptProposedAction()
