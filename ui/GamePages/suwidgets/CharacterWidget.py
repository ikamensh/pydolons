from PySide2 import QtCore, QtWidgets

from game_objects.battlefield_objects import base_attributes


class CharacterWidget(QtWidgets.QWidget):
    """docstring for CharacterPage."""
    def __init__(self, page, parent = None):
        super(CharacterWidget, self).__init__(parent)
        self.gamePages = page.gamePages
        self.character = page.gamePages.gameRoot.lengine.character
        self.btns = {}
        self.setUpWidgets()

    def setUpWidgets(self):
        self.buttonStyle = 'QPushButton{background-color:grey;color:black;}QPushButton:pressed{background-color:white;color:black;}'

        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        mainLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout()
        mainLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        mainLayout.addLayout(self.getHeroLayout(self), 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        mainLayout.addLayout(self.getPointLayout(self), 0, 1, 1, 2, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.setLayout(mainLayout)


    def getHeroLayout(self, parent):
        hero = self.gamePages.gameRoot.game.the_hero
        layout = QtWidgets.QGridLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)
        layout.setColumnMinimumWidth(0, 70)
        icon = QtWidgets.QLabel(parent)
        pixmap = self.gamePages.gameRoot.cfg.getPicFile(hero.icon, 101002002)
        icon.setPixmap(pixmap)
        icon.setFixedSize(pixmap.size())
        layout.addWidget(icon, 0, 0, 1, 2, QtCore.Qt.AlignLeft)
        self.healthBar = self.getHeroItemBar(layout, parent, 1, 'Health:')
        self.manaBar = self.getHeroItemBar(layout, parent, 2, 'Mana:')
        self.staminaBar = self.getHeroItemBar(layout, parent, 3, 'Stamina:')
        return layout

    def getHeroItemBar(self, layout, parent, row, name):
        label = QtWidgets.QLabel(name, parent)
        label.setFixedWidth(50)
        layout.addWidget(label, row, 0, 1, 1, QtCore.Qt.AlignLeft)
        bar = QtWidgets.QProgressBar(parent)
        bar.setFixedWidth(100)
        bar.setTextVisible(False)
        layout.addWidget(bar, row,  1, 1, 1, QtCore.Qt.AlignLeft)
        barLabel = QtWidgets.QLabel('', parent)
        barLabel.setFixedWidth(50)
        layout.addWidget(barLabel, row, 2, 1, 1, QtCore.Qt.AlignLeft)
        bar.setProperty('label', barLabel)
        return bar

    def getAttributeLayout(self, attribute, parent):
        layout = QtWidgets.QVBoxLayout()
        subLayout = QtWidgets.QHBoxLayout()
        pixmap = self.gamePages.gameRoot.cfg.getPicFile(str(attribute.name).lower() + '.png', 101002001)
        pixmap = pixmap.scaled(32, 32)
        icon = QtWidgets.QLabel(parent)
        icon.setPixmap(pixmap)
        icon.setFixedSize(pixmap.size())
        subLayout.addWidget(icon)
        spnBox = QtWidgets.QSpinBox(parent=parent)
        spnBox.setMinimum(self.character.base_type.attributes[attribute])
        spnBox.valueChanged.connect(self.freePointsChanged)
        spnBox.setProperty('attribute', attribute)
        self.btns[attribute] = spnBox
        subLayout.addWidget(spnBox)
        label = QtWidgets.QLabel(str(attribute.name), parent)
        layout.addLayout(subLayout)
        layout.addWidget(label)
        return layout

    def getPointLayout(self, parent):
        layout = QtWidgets.QGridLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.freePointLabel = QtWidgets.QLabel(parent = parent)
        self.freePointLabel.setText('Free points: '+ str(self.character.free_attribute_points))
        layout.addWidget(self.freePointLabel, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        i = 1
        row = 1
        for attribute in base_attributes:
            if i % 2 == 0:
                col = 0
            else:
                col = 1
                row += 1
            layout.addLayout(self.getAttributeLayout(attribute, parent), row, col)
            i += 1
        return layout

    def updatePage(self):
        hero = self.gamePages.gameRoot.game.the_hero
        self.healthBar.setMaximum(hero.max_health)
        self.healthBar.setValue(hero.health)
        self.healthBar.property('label').setText(str(int(hero.health)))
        self.manaBar.setMaximum(hero.max_mana)
        self.manaBar.setValue(hero.mana)
        self.manaBar.property('label').setText(str(int(hero.mana)))
        self.staminaBar.setMaximum(hero.max_stamina)
        self.staminaBar.setValue(hero.stamina)
        self.staminaBar.property('label').setText(str(int(hero.stamina)))
        self.freePointLabel.setText('Free points: ' + str(self.character.free_attribute_points))
        for k, v in self.character.base_type.attributes.items():
            spnBtn = self.btns.get(k)
            if not spnBtn is None:
                spnBtn.setValue(v)

    def freePointsChanged(self, value):
        spnBox = self.focusWidget()
        if self.character.temp_attributes is None:
            attributes = self.character.base_type.attributes
        else:
            attributes = self.character.temp_attributes

        if attributes[spnBox.property('attribute')] == value:
            return
        elif attributes[spnBox.property('attribute')] > value:
            self.character.reduce_attrib(spnBox.property('attribute'))
        else:
            self.character.increase_attrib(spnBox.property('attribute'))
            if self.character.free_attribute_points == 0:
                spnBox.setValue(attributes[spnBox.property('attribute')])
        self.freePointLabel.setText('Free points: ' + str(self.character.free_attribute_points))






