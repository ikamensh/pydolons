from PySide2 import QtCore, QtWidgets


class Animations:
    """
    Можно переопределить или добавить некоторые свойства
    # animation.setTargetObject(target)
    # animation.setPropertyName(b'qangel')

    Установка значения длительности воспроизведения анимации
    1000 = 1 секунда
    animation.setDuration(500)

    Без данного подключения к сигналу в объектах значение не изменяется
    animation.valueChanged.connect(target.setQAngel)

    target должен быть унаследован от QObject

    Класс Direction для примера
    class Direction(QtCore.QObject, QtWidgets.QGraphicsPixmapItem):
        def __init__(self, parent = None):
            QtCore.QObject.__init__(self, parent)
            QtWidgets.QGraphicsPixmapItem.__init__(self, parent)
            # Без установки проперти объект анимации не сможет изменять значения
            self.setProperty('qangel', 0.0)
        # Слот которы будет вызываться от сигнала.
        def setQAngel(self, angel):
            self.setRotation(angel)
    """

    @staticmethod
    def getDirectionAnim(target):
        animation = QtCore.QPropertyAnimation(target, b'angle')
        animation.setDuration(500)
        animation.valueChanged.connect(target.setQAngle)
        return animation
