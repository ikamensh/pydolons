from PySide2 import QtCore

class DemoGameTread(QtCore.QThread):

    finished = QtCore.Signal(str)

    def __init__(self, ):
        super(DemoGameTread, self).__init__()

    def setGame(self, game):
        self.game = game

    def createDemoDungeon(self):
        time = self.game.loop()
        return time

    def run(self):
        self.finished.emit(self.createDemoDungeon())
