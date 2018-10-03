from ui.GamePages.widgets import Button, BoxValue, SpinBox

class WidgetFactory(object):
    """docstring for WidgetFactory."""
    def __init__(self, gameconfig):
        super(WidgetFactory, self).__init__()
        self.gameconfig = gameconfig
        self.widgets = {}

    def createSpinBox(self, text, name = None,  w = 170, h = 39, value = 0, step = 1, max_v = 9999, min_v = 0):
        if name is None:
            name = 'spn_bx_' + str(len(self.widgets) + 1)
        spinbox = SpinBox(name, text, w, h,  value ,step, max_v, min_v)
        spinbox.setUp(self.gameconfig)
        self.widgets[name] = spinbox
        return spinbox

    def createButton(self, text, name = None, w = 100, h = 20):
        if name is None:
            name = 'btn_' + str(len(self.widgets) + 1)
        button = Button(name, text, w, h)
        self.widgets[name] = button
        return button

    def createBoxValue(self, name = None, w = 100, h = 20):
        if name is None:
            name = 'bxValue_' + str(len(self.widgets) + 1)
        boxValue = BoxValue(name, w, h)
        self.widgets[name] = boxValue
        return boxValue

    def collisions(self, pos):
        for widget in self.widgets.values():
            widget.collision(pos)

    def release(self):
        for widget in self.widgets.values():
            widget.release()
