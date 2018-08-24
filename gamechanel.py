
class GameChanel(object):
    """docstring for GameChanel."""
    def __init__(self):
        super(GameChanel, self).__init__()
        self.message = {}

    def sendMessage(self, message):
        self.message = message

    def getMessage(self):
        message = self.message
        self.message = {}
        return message

gamechanel = GameChanel()
