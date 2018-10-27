import sys
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, \
    QVBoxLayout, QFormLayout, QLabel, QFrame, QGroupBox, QRadioButton

from PySide2 import QtWidgets
from PySide2 import QtGui
from cntent.dungeons.small_orc_cave import small_orc_cave
from cntent.dungeons.pirate_lair import pirate_lair
from cntent.dungeons.demo_dungeon import demo_dungeon
from cntent.dungeons.demo_dungeon_walls import walls_dungeon
from cntent.dungeons.small_graveyard import small_graveyard

from DreamGame import DreamGame

from ui.GameConfiguration import GameConfiguration


# Every Qt application must have one and only one QApplication object;
# it receives the command line arguments passed to the script, as they
# can be used to customize the application's appearance and behavior
qt_app = QApplication(sys.argv)

gc = GameConfiguration()

class DungeonWidget(QFrame):
    def __init__(self, dungeon, parent = None):
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

    def run(self):
        # Show the form
        self.show()
        # Run the qt application
        qt_app.exec_()



class ManyDungeonsWidget(QGroupBox):
    def __init__(self, dung_list, parent=None):
        QGroupBox.__init__(self, parent)

        layout = QtWidgets.QGridLayout()
        for i, d in enumerate(dung_list):
            dung_widg = DungeonWidget(d)
            layout.addWidget(dung_widg, i // 2, i%2)

        self.setLayout(layout)

    def run(self):
        # Show the form
        self.show()
        # Run the qt application
        qt_app.exec_()



# Create an instance of the application window and run it
if __name__ == "__main__":
    app = ManyDungeonsWidget([small_orc_cave, pirate_lair, small_graveyard, demo_dungeon, walls_dungeon])
    app.run()