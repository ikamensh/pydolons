class WidgetFactory(object):
    """docstring for WidgetFactory."""
    def __init__(self, gameconfig):
        super(WidgetFactory, self).__init__()
        self.page = None
        self.gameconfig = gameconfig
        self.widgets = {}

    def collisions(self, pos):
        for widget in self.widgets.values():
            widget.collision(pos)

    def release(self):
        for widget in self.widgets.values():
            widget.release()

    def update(self):
        for widget in self.widgets.values():
            widget.update()

    def destroy(self):
        widgets = list(self.widgets.values())
        for widget in widgets:
            widget.page = None
        widgets = {}
