import my_context

class GameChanel(object):
    """docstring for GameChanel."""
    def __init__(self):
        super(GameChanel, self).__init__()
        self.message = {}
        self.msg_stack = []

    def sendMessage(self, message):
        if not my_context.the_game.is_sim:
            self.msg_stack.append(message)

gamechanel = GameChanel()
