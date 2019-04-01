from PySide2 import QtCore, QtGui

from ui.GamePages.suwidgets.ToolTip import ToolTip
from ui.GamePages.suwidgets.NotifyText import NotifyText

from abc import abstractmethod

class SuWidgetFactory:
    """docstring for SuWidgetFactory."""
    def __init__(self):
        pass

    @abstractmethod
    def getToolTip(gameRoot, w = 128, h = 128, minimumLeters = 16, pointSize = 16, opacity = 0.8):
        tooltip = ToolTip(gameRoot)
        tooltip.minimumLeters = minimumLeters
        tooltip.setBrush(QtGui.QBrush(QtCore.Qt.black))
        tooltip.setOpacity(opacity)
        tooltip.setDefaultTextColor(QtCore.Qt.white)
        font = gameRoot.cfg.getFont()
        font.setPointSize(int(pointSize * gameRoot.cfg.scale_x))
        tooltip.setFont(font)
        tooltip.setTextPos(w / 2, -h / 2)
        tooltip.setVisible(False)
        return tooltip

    def getNotifyText(gameRoot):
        notifytext = NotifyText()
        font = gameRoot.cfg.getFont()
        font.setPointSize(int(48 * gameRoot.cfg.scale_x))
        notifytext.setFont(font)
        notifytext.setDefaultTextColor(QtCore.Qt.blue)
        notifytext.gameRoot = gameRoot
        gameRoot.view.wheel_change.connect(notifytext.resized)
        return notifytext
