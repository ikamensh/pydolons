from enum import Enum, auto

class LogTargets(Enum):
    FILE = auto()
    PRINT = auto()
    SILENT = auto()

class GameLog:
    the_log = None

    def __init__(self, target):
        assert target in LogTargets
        self.target = target
        GameLog.the_log = self

    def __call__(self, msg):
        if self.target == LogTargets.SILENT:
            return
        elif self.target == LogTargets.PRINT:
            print(msg)
        elif self.target == LogTargets.FILE:
            raise NotImplemented

gamelog = GameLog(LogTargets.SILENT)

