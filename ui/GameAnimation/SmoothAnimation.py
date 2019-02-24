from collections import deque
from PySide2 import QtCore
from ui.GameAnimation.GameVariantAnimation import GameVariantAnimation


class SmoothAnimation:
    """
    Этот класс накапливает требуемые анимации и проигрывает их с увеличеной скоростью.
    Для единичных анимаций скорость равна базовой скорости.

    Для использования класса необходимо указать слот изменения контроллируемого аттрибута,
    например QObject.setRotation для угра поворота. Дальше достаточно просто вызывать play_anim(start, end)
    """
    def __init__(self, target, slot, basic_duration = GameVariantAnimation.DURATION_BASIC):
        self.basic_duration = basic_duration

        self.anim = GameVariantAnimation(target)
        self.anim.valueChanged.connect(slot)
        self.anim.stateChanged.connect(self._keep_playing)
        self.queue = deque()

    def _keep_playing(self, state):

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
