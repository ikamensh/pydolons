from PySide2 import QtWidgets

class HealthBar(QtWidgets.QGraphicsRectItem):
    """docstring for HealtBar."""
    def __init__(self):
        super(HealthBar, self).__init__()
        self.setOpacity(0.6)

    def setHP(self, hp):
        """ По указанным процентам устанавливает длину HealtBar
        делим на 7 частей
        1/7 -- высоты героя
        6/7 -- начало отсчета
        """

        w = int(128 * hp / 100)
        h = 128 / 7
        y = (6 * 128) / 7
        self.rect().setWidth(w)
        self.setRect(0, y, w, h)
