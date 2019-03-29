from enum import Enum, auto
from contextlib import contextmanager


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
        self.msg = None

    def __call__(self, msg):
        if self.target == LogTargets.SILENT:
            return
        elif self.target == LogTargets.PRINT:
            print(msg)
            self.msg = msg
        elif self.target == LogTargets.FILE:
            raise NotImplemented

    def mute(self):
        self.target = LogTargets.SILENT

# gamelog = GameLog(LogTargets.PRINT)
# gamelog = GameLog(LogTargets.SILENT)
