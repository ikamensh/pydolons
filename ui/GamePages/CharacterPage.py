from PySide2 import QtCore, QtGui, QtWidgets

from character_creation.Character import Character
from game_objects.battlefield_objects.BaseType import BaseType

from ui.GamePages.widgets import WidgetFactory
from ui.GamePages import AbstractPage

class CharacterPage(AbstractPage):
    """docstring for CharacterPage."""
    def __init__(self):
        super(CharacterPage, self).__init__()
        self.character = None
        self.w, self.h = 790, 590
        self.w_2 = int(self.w / 2)
        self.h_2 = int(self.h / 2)


    def setUpGui(self):
        self.setUpWidgets()

    def pageUpdate(self):
        self.update( self.x(), self.y(), self.w, self.h)
        self.widgetFactory.update()

    def setUpWidgets(self):
        x, y = 264, 18
        n = 40
        m = 150
        self.widgetFactory = WidgetFactory(self.gamePages.gameRoot.cfg)
        self.widgetFactory.page =self
        self.spn_bx1 = self.widgetFactory.createSpinBox('STREINGTH')
        self.spn_bx1.setPos(x, n)
        self.spn_bx2 = self.widgetFactory.createSpinBox('AGILITY')
        self.spn_bx2.setPos( x,  n * 2 +5)
        self.spn_bx3 = self.widgetFactory.createSpinBox('ENDURANCE')
        self.spn_bx3.setPos( x,  n * 3 + 10)
        self.spn_bx4 = self.widgetFactory.createSpinBox('INTELLIGENCE')
        self.spn_bx4.setPos(x,  n * 4 + 15)
        self.spn_bx5 = self.widgetFactory.createSpinBox('PERCEPTION')
        self.spn_bx5.setPos( x,  n * 5 + 20)
        self.spn_bx6 = self.widgetFactory.createSpinBox('CHARISMA')
        self.spn_bx6.setPos( x,  n * 6 + 25)
        # Button quit
        self.btn_quit = self.widgetFactory.createButton('X', w = 30, h = 20)
        self.btn_quit.setPos( self.w - 40,  10)
        self.btn_quit.presed.connect(self.onPressClose)
        # Button ok
        self.btn_ok = self.widgetFactory.createButton('ok', w = 60, h = 20)
        self.btn_ok.setPos(40,  self.h - 40)
        self.btn_ok.presed.connect(self.onPressOk)
        # Button cancel
        self.btn_cancel = self.widgetFactory.createButton('cancel', w = 60, h = 20)
        self.btn_cancel.setPos(110, self.h - 40)
        self.btn_cancel.presed.connect(self.onPressCancel)
        # Box value
        self.bx_hp = self.widgetFactory.createBoxValue()
        self.bx_hp.setPos( 100,  295)
        self.bx_mana = self.widgetFactory.createBoxValue()
        self.bx_mana.setPos( 100,  335)
        self.bx_stamina = self.widgetFactory.createBoxValue()
        self.bx_stamina.setPos(100, 375)

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.white)
        painter.setBrush(QtCore.Qt.black)
        # Draw lines
        painter.drawRect(self.x(), self.y(), self.w, self.h)
        painter.drawLine(self.x() + 210, self.y(), self.x() + 210, self.y() + self.h)
        painter.drawLine(self.x() + 540, self.y(), self.x() + 540, self.y() + 350)
        painter.drawLine(self.x() + 210, self.y() + 350, self.x() + self.w, self.y() + 350)
        painter.drawLine(self.x() + 210, self.y() + 417, self.x() + self.w, self.y() + 417)
        painter.drawLine(self.x() + 416, self.y() + 417, self.x() + 416, self.y() + self.h)
        painter.drawLine(self.x() + 597, self.y() + 417, self.x() + 597, self.y() + self.h)
        # Number column
        x, y = 35, 310
        n = 40
        painter.setBrush(QtCore.Qt.green)
        painter.drawRect(self.x() + x, self.y() + 144, 128, 128)
        painter.drawText(self.x() + x, self.y() + y, 'HP:')
        self.bx_hp.paint(painter)
        painter.drawText(self.x() + x, self.y() + y + n, 'Manna:')
        self.bx_mana.paint(painter)
        painter.drawText(self.x() + x, self.y() + y + 2 * n, 'Stamina:')
        self.bx_stamina.paint(painter)
        # Two column
        x, y = 264, 18
        n = 40
        m = 150
        painter.drawText(self.x() + x, self.y() + y, 'Free point: 11')
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
        painter.drawText(self.x() + 241, self.y() + 383, 'Mastery:')
        # Tree column
        x, y = 264, 436
        n = 40
        painter.drawText(self.x() + x, self.y() + y, 'Battle')
        painter.drawText(self.x() + x, self.y() + y + n, 'Axe')
        painter.drawText(self.x() + x, self.y() + y + 2 * n, 'Sword')
        painter.drawText(self.x() + x, self.y() + y + 3 * n, 'Spear')
        # Four column
        x, y = 437, 436
        n = 40
        painter.drawText(self.x() + x, self.y() + y, 'Magic')
        painter.drawText(self.x() + x, self.y() + y + n, 'Ice')
        painter.drawText(self.x() + x, self.y() + y + 2 * n, 'Fire')
        painter.drawText(self.x() + x, self.y() + y + 3 * n, 'Lighting')
        # Fice column
        x, y = 647, 436
        n = 40
        painter.drawText(self.x() + x, self.y() + y, 'Mics')
        painter.drawText(self.x() + x, self.y() + y + n, 'Alchemy')
        # Q_UNUSED(option)
        # Q_UNUSED(widget)
        # pass

    def boundingRect(self):
        return QtCore.QRectF(self.x() , self.y(), self.w, self.h)

    def onPressClose(self):
        self.state = False
        self.gamePages.page = None
        self.scene().removeItem(self)

    def collisions(self, pos):
            self.widgetFactory.collisions(pos)
            self.pageUpdate()

    def release(self):
            self.widgetFactory.release()
            self.pageUpdate()



    def onPressCancel(self):
        # self.state = False
        # self.scene().removeItem(self)
        pass

    def onPressOk(self):
        # self.state = False
        # self.scene().removeItem(self)
        pass
