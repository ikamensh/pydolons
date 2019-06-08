from __future__ import annotations
from mechanics.events import Event as GameEvent
from PySide2 import QtCore
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from DreamGame import DreamGame
    from ui.TheUI import TheUI


class ProxyEmit(object):
    """
    Этот класс проксирует вызов сизнала в логический движок the_game.
    Сигналы срабатывают внутри тригеров.

    # Метод play_movement_anim обрабатывает вызов MovementEvent
    def play_movement_anim(t, e):
        # вызов проксированного сигнала
        ProxyEmit.play_movement_anim.emit({'unit':e.unit,"cell_to":e.cell_to})
        pass

    # Триггер для вызова метода play_movement_anim
    def move_anim_trigger():
        return Trigger(MovementEvent,
                       conditions={/no_sim_condition},
                       callbacks=[play_movement_anim])

    """
    log_event: QtCore.Signal = None
    play_movement_anim: QtCore.Signal = None
    maybe_play_damage_anim: QtCore.Signal = None
    maybe_play_hit_anim: QtCore.Signal = None
    play_attack_anim: QtCore.Signal = None
    play_perish_anim: QtCore.Signal = None
    play_trun_anim: QtCore.Signal = None
    play_nextunit_anim: QtCore.Signal = None
    play_levelstatus: QtCore.Signal = None
    obstacle_destroyed: QtCore.Signal = None

    def __init__(self, arg):
        super(ProxyEmit, self).__init__()


class GameLoopThread(QtCore.QThread):
    """
    """
    # Инициализация сигналов
    play_movement_anim = QtCore.Signal(dict)
    maybe_play_damage_anim = QtCore.Signal(dict)
    maybe_play_hit_anim = QtCore.Signal(dict)
    play_attack_anim = QtCore.Signal(dict)
    play_perish_anim = QtCore.Signal(dict)
    play_trun_anim = QtCore.Signal(dict)
    play_nextunit_anim = QtCore.Signal()
    play_levelstatus = QtCore.Signal(str)
    obstacle_destroyed = QtCore.Signal(dict)
    log_event = QtCore.Signal(GameEvent)

    def __init__(self, parent=None):
        super(GameLoopThread, self).__init__(parent)
        self.game: DreamGame = None
        self.the_ui: TheUI = None

    def setSiganls(self, proxy_cls: ProxyEmit):
        """
        Здесь сигналы проксируются

        Здесь происходит присоединение слотов к сигналам
        self.setConnection()
        """
        proxy_cls.play_movement_anim = self.play_movement_anim
        proxy_cls.maybe_play_damage_anim = self.maybe_play_damage_anim
        proxy_cls.maybe_play_hit_anim = self.maybe_play_hit_anim
        proxy_cls.play_attack_anim = self.play_attack_anim
        proxy_cls.play_perish_anim = self.play_perish_anim
        proxy_cls.play_trun_anim = self.play_trun_anim
        proxy_cls.play_nextunit_anim = self.play_nextunit_anim
        proxy_cls.play_levelstatus = self.play_levelstatus
        proxy_cls.obstacle_estroyed = self.obstacle_destroyed
        proxy_cls.log_event = self.log_event
        # Здесь происходит присоединение слотов к сигналам
        self.setConnection()

    def setConnection(self):
        self.play_movement_anim.connect(self.the_ui.gameRoot.level.units.unitMoveSlot)
        self.maybe_play_damage_anim.connect(self.the_ui.gameRoot.level.units.targetDamageSlot)
        self.maybe_play_hit_anim.connect(self.the_ui.gameRoot.level.units.targetDamageHitSlot)
        self.play_attack_anim.connect(self.the_ui.gameRoot.level.units.attackSlot)
        self.play_perish_anim.connect(self.the_ui.gameRoot.level.units.unitDiedSlot)
        self.play_trun_anim.connect(self.the_ui.gameRoot.level.units.unitTurnSlot)
        self.play_nextunit_anim.connect(self.the_ui.gameRoot.gamePages.gameMenu.update_unitsStack)
        self.play_levelstatus.connect(self.the_ui.gameRoot.level.setStatus)
        self.log_event.connect(self.the_ui.gameRoot.controller.send_game_event)
        self.obstacle_destroyed.connect(self.debug)

    def run(self):
        self.game.loop()

    def debug(self, msg):
        print('DEBUG MSG', msg)

