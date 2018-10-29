from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import QFormLayout, QLabel, QFrame, QRadioButton


from DreamGame import DreamGame


class DungeonWidget(QFrame):

    selected = Signal(object)
    deselected = Signal()

    def __init__(self, dungeon, parent = None, gc=None):
        QFrame.__init__(self, parent)


        self.rbutton = QRadioButton(self)

        # self.setFrameShadow(QFrame.Raised)
        self.setObjectName("DungeonFrame")
        self.setStyleSheet("#DungeonFrame {border: 2px solid black}")
        self.dungeon = dungeon

        # Create the form layout that manages the labeled controls
        self.form_layout = QFormLayout()

        icon = QLabel()
        icon.setPixmap(gc.getPicFile(dungeon.icon))
        self.form_layout.addRow(icon)

        self.form_layout.addRow(QLabel(dungeon.name))

        locs = dungeon.unit_locations(DreamGame())

        self.n_units_label = QLabel(f'{len([u for u in locs.keys() if not u.is_obstacle])}', self)
        self.form_layout.addRow('Units in the dungeon:', self.n_units_label)

        self.max_xp_label = QLabel(f'{max([u.xp for u in locs.keys() if not u.is_obstacle])}', self)
        self.form_layout.addRow('Strongest enemy XP: ', self.max_xp_label)
        self.form_layout.addWidget(self.rbutton)

        self.setLayout(self.form_layout)

        self.rbutton.toggled.connect(self.toggled)

    @Slot()
    def toggled(self, selected):
        if selected:
            self.selected.emit(self)
        else:
            self.deselected.emit()