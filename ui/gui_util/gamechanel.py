import my_context

class GameChanel(object):
    """docstring for GameChanel."""
    def __init__(self):
        super(GameChanel, self).__init__()
        self.message = {}
        self.msg_stack = []

    def sendMessage(self, message):
        # self.message = message
        if not my_context.the_game.is_sim:
            self.msg_stack.append(message)

    # def getMessage(self):
    #     # print(self.msg_stack)
    #     # print('->'.join([msg.get('event') for msg in self.msg_stack ]))
    #     message = self.message
    #     self.message = {}
    #     return message

gamechanel = GameChanel()
