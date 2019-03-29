from PySide2.QtCore import QVariantAnimation


class GameVariantAnimation(QVariantAnimation):
    DURATION_BASIC = 500
    DURATION_UNIT_MOVE = 300

    def __init__(self, parent):
        super(GameVariantAnimation, self).__init__(parent)
        self.setDuration(self.DURATION_BASIC)
