from PySide2 import QtCore
from ui.gui_util.gamechanel import gamechanel

class GameProxyChanel(QtCore.QObject):
    """docstring for GameChanel.
    Данный класс генерирует сигналы о событиях
    """
    attackTo = QtCore.Signal(dict)
    unitActive = QtCore.Signal(dict)
    unitDied = QtCore.Signal(dict)
    unitMove = QtCore.Signal(dict)
    unitTurn = QtCore.Signal(dict)
    targetDamage = QtCore.Signal(dict)
    def __init__(self):
        super(GameProxyChanel, self).__init__()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.slotAlarmTimer)
        self.timer.start(10)

    def slotAlarmTimer(self):
        self.slotStackWork()
        # message = gamechanel.getMessage()
        # # if message != {}:
        # #     print(message)
        # if message.get('event') == 'UnitDiedEvent':
        #     self.unitDied.emit(message)
        # elif message.get('event') == 'MovementEvent':
        #     self.unitMove.emit(message)
        # elif message.get('event') == 'DamageEvent':
        #     self.targetDamage.emit(message)
        # elif message.get('event') == 'AttackEvent':
        #     self.attackTo.emit(message)

    def slotStackWork(self):
        while gamechanel.msg_stack:
            message = gamechanel.msg_stack.pop(0)
            if message.get('event') == 'UnitDiedEvent':
                self.unitDied.emit(message)
            elif message.get('event') == 'ActiveEvent':
                self.unitActive.emit(message)
            elif message.get('event') == 'TurnEvent':
                self.unitTurn.emit(message)
            # elif message.get('event') == 'MovementEvent':
                # self.unitMove.emit(message)
            # elif message.get('event') == 'DamageEvent':
                # self.targetDamage.emit(message)
            # elif message.get('event') == 'AttackEvent':
            #     self.attackTo.emit(message)



    def sendMessage(self, message):
        self.message = message

    def getMessage(self):
        message = self.message
        self.message = {}
        return message
