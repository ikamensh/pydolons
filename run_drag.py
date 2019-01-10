import sys
from PySide2 import QtGui, QtCore, QtWidgets

class SlotWidget(QtWidgets.QLabel):

    def __init__(self,*args, parent = None):
        super(SlotWidget, self).__init__(*args, parent=parent)
        self.start_point = QtCore.QPoint()
        self.dragStart = QtCore.QPoint()
        self.setAcceptDrops( True )
        self.setStyleSheet('background-color:rgba(127, 127, 127, 100);')

    def mousePressEvent(self, ev):
        self.dragStart = ev.pos()
        pass

    def mouseMoveEvent(self, ev):
        if ev.buttons() == QtCore.Qt.LeftButton:
            if QtWidgets.QApplication.startDragDistance() <= (ev.pos() - self.dragStart ).manhattanLength():
                # self.move(ev.pos())
                self.startDrag()

    def startDrag(self):
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        # mimeData.setImageData(getPixmap().toImage());
        mimeData.setText(self.text());
        drag.setMimeData(mimeData);
        # drag->setPixmap(getPixmap());

        result = drag.start(QtCore.Qt.MoveAction)
        print("Drop action result: ", result)
        if result == QtCore.Qt.CopyAction:
            self.setText('empty')
        if result == QtCore.Qt.MoveAction:
            self.setText('empty')

    def onLoadImage(self):
        print('run onLoadImage')
        pass

    def dragEnterEvent(self, ev:QtGui.QDragEnterEvent):
        formats = ev.mimeData().formats()

        print('formats', formats)
        if "text/plain" in formats:
            ev.acceptProposedAction()

    def dropEvent(self, ev:QtGui.QDropEvent):
        self.setText(ev.mimeData().text())
        ev.acceptProposedAction()

class Button(QtWidgets.QPushButton):

    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent)

    def mouseMoveEvent(self, e):

        if e.buttons() != QtCore.Qt.LeftButton:
            return

        mimeData = QtCore.QMimeData()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.start(QtCore.Qt.MoveAction)

    def mousePressEvent(self, e):

        QtWidgets.QPushButton.mousePressEvent(self, e)
        if e.button() == QtCore.Qt.LeftButton:
            print
            'press'


class Example(QtWidgets.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        layout = QtWidgets.QVBoxLayout()
        for i in range(10):
            w = SlotWidget('slot_'+str(i+1))
            layout.addWidget(w)
        # self.btn = Button('Button', self)
        # self.btn.move(100, 65)
        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Click or move')
        self.show()

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        # self.btn.move(position)

        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()