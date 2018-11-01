from collections import deque
from PySide2 import QtCore, QtWidgets


class SmoothAnimation:
    """
    Этот класс накапливает требуемые анимации и проигрывает их с увеличеной скоростью.
    Для единичных анимаций скорость равна базовой скорости.

    Для использования класса необходимо указать слот изменения контроллируемого аттрибута,
    например QObject.setRotation для угра поворота. Дальше достаточно просто вызывать play_anim(start, end)
    """
    def __init__(self, target, slot, basic_duration = 500):
        self.basic_duration = basic_duration
        anim = QtCore.QPropertyAnimation(target, b'angle')
        anim.setDuration(basic_duration)

        anim.valueChanged.connect(slot)
        anim.stateChanged.connect(self._keep_playing)

        self.anim = anim


        self.queue = deque()

    def _keep_playing(self, state):
        print(state, self.queue)

        if state == QtCore.QAbstractAnimation.Stopped:
            if self.queue:
                start, end = self.queue.popleft()
                self.anim.setDuration(self.basic_duration / (2 + len(self.queue)))
                self.anim.setStartValue(start)
                self.anim.setEndValue(end)
                self.anim.start()


    def play_anim(self, start, end):
        if self.anim.state() == QtCore.QAbstractAnimation.Stopped:
            self.anim.setDuration(self.basic_duration)
            self.anim.setStartValue(start)
            self.anim.setEndValue(end)
            self.anim.start()
        else:
            self.queue.append((start, end))
            self.anim.setDuration(self.basic_duration / (2 + len(self.queue)))