from PySide2 import QtCore, QtGui, QtWidgets

from ui.GamePages.suwidgets.ToolTip import ToolTip
from ui.GamePages.suwidgets.NotifyText import NotifyText

from abc import abstractmethod

class SuWidgetFactory:
    """docstring for SuWidgetFactory."""
    def __init__(self):
        pass

    @abstractmethod
    def getToolTip(gameRoot, w = 128, h = 128, minimumLeters = 16, fontFamily = "Times", pointSize = 12, opacity = 0.8):
        tooltip = ToolTip(gameRoot)
        tooltip.minimumLeters = minimumLeters
        tooltip.setBrush(QtGui.QBrush(QtCore.Qt.black))
        tooltip.setOpacity(opacity)
        tooltip.setDefaultTextColor(QtCore.Qt.white)
        tooltip.setFont(QtGui.QFont(fontFamily, pointSize, 10, False))
        tooltip.setTextPos(w / 2, -h / 2)
        tooltip.setVisible(False)
        return tooltip

    def getNotifyText(gameRoot):
        notifytext = NotifyText()
        notifytext.setFont(QtGui.QFont("Times", 48, 10, False))
        notifytext.setDefaultTextColor(QtCore.Qt.blue)
        notifytext.gameRoot = gameRoot
        gameRoot.view.wheel_change.connect(notifytext.resized)
        return notifytext
