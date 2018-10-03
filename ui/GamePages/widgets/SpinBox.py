from ui.GamePages.widgets import AbstactWidget

class SpinBox(AbstactWidget):
    """docstring for SpinBox."""
    def __init__(self, name, text,  w = 170, h = 39,  value = 0, step = 1, max_v = 9999, min_v = 0):
        super(SpinBox, self).__init__(name, w, h)
        self.data = {'btn_up': True,
                    'btn_down': True,
                    'value': value,
                    'step': step,
                    'max_v':max_v,
                    'min_v':min_v,
                    'last_min':None,
                    'last_max':None,
                    'last_v':None,
                    'name':name,
                    'text':text
                    }

    def setUp(self, gameconfig):
        self.gameconfig = gameconfig

    def paint(self, painter, option = None, widget = None):
        painter.drawText(self.x, self.y + 22, self.data['text'])
        painter.drawText(self.x + 150, self.y + 22, str(self.data['value']))
        if self.data['btn_up']:
            painter.drawPixmap(self.x + 100, self.y + 1 , self.gameconfig.getPicFile('up4.png'))
        else:
            painter.drawPixmap(self.x + 100, self.y + 1  , self.gameconfig.getPicFile('up4.png').scaled(25, 16))
        if self.data['btn_down']:
            painter.drawPixmap(self.x + 100, self.y + 21 , self.gameconfig.getPicFile('down4.png'))
        else:
            painter.drawPixmap(self.x + 100, self.y + 21 , self.gameconfig.getPicFile('down4.png').scaled(25, 16))

    def collision(self, pos):
        if pos.y() > self.y + 21 and pos.y() < self.y + 38 and pos.x() > self.x + 100 and  pos.x() < self.x + 127:
            self.data['btn_down'] = False
            self.data['last_v'] = self.data['value']
            self.data['value']-=self.data['step']
            if self.data['value'] < self.data['min_v'] or self.data['value'] > self.data['max_v']:
                self.data['value'] = self.data['last_v']
        if pos.y() > self.y + 1 and pos.y() < self.y + 17 and pos.x() > self.x + 100 and  pos.x() < self.x + 127:
            self.data['btn_up'] = False
            self.data['last_v'] = self.data['value']
            self.data['value']+=self.data['step']
            if self.data['value'] < self.data['min_v'] or self.data['value'] > self.data['max_v']:
                self.data['value'] = self.data['last_v']

    def release(self):
        self.data['btn_down'] = True
        self.data['btn_up'] = True
