"""
В это пакете находятся вызываемые страницы.
Страницы создаются один раз при загрузке игры.
Страницы обновляются по мере необходимости.
"""

class GamePages(object):
    """docstring for GamePages."""
    def __init__(self):
        super(GamePages, self).__init__()
    self.gameRoot = None

    def setGameRoot(self, gameRoot):
        self.gameRoot =  gameRoot
