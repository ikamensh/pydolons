from PySide2 import QtWidgets, QtCore, QtGui


class SlotContextMenu(QtWidgets.QMenu):
    def __init__(self, page, parent):
        super(SlotContextMenu, self).__init__(parent=parent)
        self.page = page
        self.cfg = page.pages.gameRoot.cfg
        self.use = QtWidgets.QAction('Use', self)
        self.info = QtWidgets.QAction('Info', self)
        self.edit = QtWidgets.QAction('Edit', self)
        self.drop = QtWidgets.QAction('Drop', self)

    def usedItem(self):
        print('used_item')
