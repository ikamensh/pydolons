from PySide2 import QtCore
from ui.gui_util.gamechanel import gamechanel

class GameProxyChanel(QtCore.QObject):
    """docstring for GameChanel.
    Данный класс генерирует сигналы о событиях
    """
    attackTo = QtCore.Signal(dict)
    unitDied = QtCore.Signal(dict)
    unitMove = QtCore.Signal(dict)
    targetDamage = QtCore.Signal(dict)
    def __init__(self):
        super(GameProxyChanel, self).__init__()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.slotAlarmTimer)
        self.timer.start(10)

    def slotAlarmTimer(self):
        message = gamechanel.getMessage()
        # if message != {}:
        #     print(message)
        if message.get('event') == 'UnitDiedEvent':
            self.unitDied.emit(message)
        if message.get('event') == 'MovementEvent':
            self.unitMove.emit(message)
        if message.get('event') == 'DamageEvent':
            self.targetDamage.emit(message)
        if message.get('event') == 'AttackEvent':
            self.attackTo.emit(message)


    def sendMessage(self, message):
        self.message = message

    def getMessage(self):
        message = self.message
        self.message = {}
        return message
