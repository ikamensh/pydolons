from PySide2 import QtCore, QtGui, QtWidgets

from character_creation.Character import Character
from game_objects.battlefield_objects.BaseType import BaseType

from ui.GamePages.widgets import WidgetFactory
from ui.GamePages import AbstractPage

class CharacterPage(AbstractPage):
    """docstring for CharacterPage."""
    def __init__(self):
        super(CharacterPage, self).__init__()
        # self.model = None
        self.w, self.h = 860, 640
        self.w_2 = int(self.w / 2)
        self.h_2 = int(self.h / 2)
        self.w_2 = 0
        self.h_2 = 0


    def setUpGui(self):
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable|QtWidgets.QGraphicsItem.ItemIsMovable|QtWidgets.QGraphicsItem.ItemIsFocusable)
        # self.setUpModel()
        self.setUpWidgets()

    def pageUpdate(self):
        # self.bx_hp.update(self.model.data['hp'], self.model.data['max_hp'])
        # self.bx_mana.update(self.model.data['mana'], self.model.data['max_mana'])
        # self.bx_stamina.update(self.model.data['stamina'], self.model.data['max_stamina'])
        self.update( -self.w_2 , - self.h_2, self.w, self.h)

    def setUpWidgets(self):
        x, y = 264, 18
        n = 40
        m = 150
        self.widgetFactory = WidgetFactory(self.gamePages.gameRoot.cfg)
        self.spn_bx1 = self.widgetFactory.createSpinBox('STREINGTH')
        self.spn_bx1.setPos(-self.w_2 + x, -self.h_2 + 40)
        self.spn_bx2 = self.widgetFactory.createSpinBox('AGILITY')
        self.spn_bx2.setPos(-self.w_2 + x, -self.h_2 + 85)
        self.spn_bx3 = self.widgetFactory.createSpinBox('ENDURANCE')
        self.spn_bx3.setPos(-self.w_2 + x, -self.h_2 + 130)
        self.spn_bx4 = self.widgetFactory.createSpinBox('INTELLIGENCE')
        self.spn_bx4.setPos(-self.w_2 + x, -self.h_2 + 175)
        self.spn_bx5 = self.widgetFactory.createSpinBox('PERCEPTION')
        self.spn_bx5.setPos(-self.w_2 + x, -self.h_2 + 220)
        self.spn_bx6 = self.widgetFactory.createSpinBox('CHARISMA')
        self.spn_bx6.setPos(-self.w_2 + x, -self.h_2 + 265)
        # Button quit
        self.btn_quit = self.widgetFactory.createButton('X', w = 30, h = 20)
        self.btn_quit.setPos(self.w_2 - 40, -self.h_2 + 10)
        self.btn_quit.presed.connect(self.onPressClose)
        # Button ok
        self.btn_ok = self.widgetFactory.createButton('ok', w = 60, h = 20)
        self.btn_ok.setPos(-self.w_2 + 40, self.h_2 - 40)
        # self.btn_ok.presed.connect(self.onPressClose)
        # Button cancel
        self.btn_cancel = self.widgetFactory.createButton('cancel', w = 60, h = 20)
        self.btn_cancel.setPos(-self.w_2 + 110, self.h_2 - 40)
        # self.btn_ok.presed.connect(self.onPressClose)
        # Box value
        self.bx_hp = self.widgetFactory.createBoxValue()
        self.bx_hp.setPos(-self.w_2 + 100, -self.h_2 + 295)
        self.bx_mana = self.widgetFactory.createBoxValue()
        self.bx_mana.setPos(-self.w_2 + 100, -self.h_2 + 335)
        self.bx_stamina = self.widgetFactory.createBoxValue()
        self.bx_stamina.setPos(-self.w_2 + 100, -self.h_2 + 375)

    def onPressClose(self):
        self.scene().removeItem(self)

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.white)
        painter.setBrush(QtCore.Qt.black)
        # Draw lines
        painter.drawRect(-self.w_2, -self.h_2, self.w, self.h)
        painter.drawLine(-self.w_2 + 210, -self.h_2, -self.w_2 + 210, self.h_2)
        painter.drawLine(-self.w_2 + 540, -self.h_2, -self.w_2 + 540, -self.h_2 + 350)
        painter.drawLine(-self.w_2 + 210, -self.h_2 + 350, self.w_2, -self.h_2 + 350)
        painter.drawLine(-self.w_2 + 210, -self.h_2 + 417, self.w_2, -self.h_2 + 417)
        painter.drawLine(-self.w_2 + 416, -self.h_2 + 417, -self.w_2 + 416, self.h_2)
        painter.drawLine(-self.w_2 + 597, -self.h_2 + 417, -self.w_2 + 597, self.h_2)
        # Number column
        x, y = 35, 310
        n = 40
        painter.setBrush(QtCore.Qt.green)
        painter.drawRect(-self.w_2 + x, -self.h_2 + 144, 128, 128)
        painter.drawText(-self.w_2 + x, -self.h_2 + y, 'HP:')
        self.bx_hp.paint(painter)
        painter.drawText(-self.w_2 + x, -self.h_2 + y + n, 'Manna:')
        self.bx_mana.paint(painter)
        painter.drawText(-self.w_2 + x, -self.h_2 + y + 2 * n, 'Stamina:')
        self.bx_stamina.paint(painter)
        # Two column
        x, y = 264, 18
        n = 40
        m = 150
        painter.drawText(-self.w_2 + x, -self.h_2 + y, 'Free point: 11')
        # Debug text

        self.spn_bx1.paint(painter)
        self.spn_bx2.paint(painter)
        self.spn_bx3.paint(painter)
        self.spn_bx4.paint(painter)
        self.spn_bx5.paint(painter)
        self.spn_bx6.paint(painter)

        self.btn_quit.paint(painter)
        self.btn_ok.paint(painter)
        self.btn_cancel.paint(painter)

        # Tree, Four, Five column
        painter.drawText(-self.w_2 + 241, -self.h_2 + 383, 'Mastery:')
        # Tree column
        x, y = 264, 436
        n = 40
        painter.drawText(-self.w_2 + x, -self.h_2 + y, 'Battle')
        painter.drawText(-self.w_2 + x, -self.h_2 + y + n, 'Axe')
        painter.drawText(-self.w_2 + x, -self.h_2 + y + 2 * n, 'Sword')
        painter.drawText(-self.w_2 + x, -self.h_2 + y + 3 * n, 'Spear')
        # Four column
        x, y = 437, 436
        n = 40
        painter.drawText(-self.w_2 + x, -self.h_2 + y, 'Magic')
        painter.drawText(-self.w_2 + x, -self.h_2 + y + n, 'Ice')
        painter.drawText(-self.w_2 + x, -self.h_2 + y + 2 * n, 'Fire')
        painter.drawText(-self.w_2 + x, -self.h_2 + y + 3 * n, 'Lighting')
        # Fice column
        x, y = 647, 436
        n = 40
        painter.drawText(-self.w_2 + x, -self.h_2 + y, 'Mics')
        painter.drawText(-self.w_2 + x, -self.h_2 + y + n, 'Alchemy')
        # Q_UNUSED(option)
        # Q_UNUSED(widget)
        # pass

    def boundingRect(self):
        return QtCore.QRectF(-self.w/2, -self.h/2, self.w, self.h)
