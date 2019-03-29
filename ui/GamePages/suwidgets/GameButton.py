from PySide2 import QtCore, QtWidgets


class GameButton(QtWidgets.QPushButton):
    hovered = QtCore.Signal(QtCore.QObject)
    hover_out = QtCore.Signal(QtCore.QObject)

    def __init__(self, *args, parent=None):
        super(GameButton, self).__init__(*args, parent)
        self.setAttribute(QtCore.Qt.WA_Hover)
        self.installEventFilter(self)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.HoverEnter:
            watched.hovered.emit(watched)
            pass
        elif event.type() == QtCore.QEvent.HoverLeave:
            watched.hover_out.emit(watched)
        return QtWidgets.QWidget.eventFilter(self, watched, event)
