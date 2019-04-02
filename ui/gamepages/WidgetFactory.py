from PySide2 import QtCore, QtGui

from ui.gamepages.suwidgets.ToolTip import ToolTip
from ui.gamepages.suwidgets.NotifyText import NotifyText


class WidgetFactory:
    """docstring for SuWidgetFactory."""
    def __init__(self):
        pass

    @staticmethod
    def getToolTip(gameRoot, w = 128, h = 128, minimumLeters = 16, pointSize = 16, opacity = 0.8)->ToolTip:
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

    @staticmethod
    def getNotifyText(gameRoot)->NotifyText:
        notifytext = NotifyText()
        font = gameRoot.cfg.getFont()
        font.setPointSize(int(48 * gameRoot.cfg.scale_x))
        notifytext.setFont(font)
        notifytext.setDefaultTextColor(QtCore.Qt.blue)
        notifytext.gameRoot = gameRoot
        gameRoot.view.wheel_change.connect(notifytext.resized)
        return notifytext
