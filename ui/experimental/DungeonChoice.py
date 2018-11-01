from __future__ import annotations
import sys
from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import QApplication, QPushButton, QGroupBox

from PySide2 import QtWidgets

from cntent.dungeons.small_orc_cave import small_orc_cave
from cntent.dungeons.pirate_lair import pirate_lair
from cntent.dungeons.demo_dungeon import demo_dungeon
from cntent.dungeons.demo_dungeon_walls import walls_dungeon
from cntent.dungeons.small_graveyard import small_graveyard

from ui.experimental.DungeonWidget import DungeonWidget



class DungeonChoice(QGroupBox):
    def __init__(self, dung_list, parent=None, gc=None):
        QGroupBox.__init__(self, parent)

        self.dungeon_widgets = []

        layout = QtWidgets.QGridLayout()
        for i, d in enumerate(dung_list):
            dung_widg = DungeonWidget(d, gc=gc)
            layout.addWidget(dung_widg, i // 2, i%2)
            self.dungeon_widgets.append(dung_widg)

            dung_widg.selected.connect(self.select_dungeon)
            dung_widg.deselected.connect(self.disable_start)

        start_button = QPushButton()
        start_button.setText("Start dungeon")
        start_button.setEnabled(False)
        start_button.clicked.connect(self.start_dungeon)

        self.start_button = start_button

        layout.addWidget(start_button)
        self.setLayout(layout)


    @property
    def selected_dungeon(self):
        for dw in self.dungeon_widgets:
            if dw.rbutton.isChecked():
                return dw.dungeon
        return None

    @Slot()
    def disable_start(self):
        self.start_button.setEnabled(False)

    @Slot()
    def start_dungeon(self):
        raise NotImplementedError

    @Slot()
    def select_dungeon(self, dung_widget):
        # print(dung_widget)
        for dw in self.dungeon_widgets:
            if dw is not dung_widget:
                dw.rbutton.setChecked(False)
        self.start_button.setEnabled(True)




if __name__ == "__main__":
    from ui.GameConfiguration import GameConfiguration

    qt_app = QApplication(sys.argv)
    gc = GameConfiguration()

    app = DungeonChoice([small_orc_cave, pirate_lair, small_graveyard, demo_dungeon, walls_dungeon], gc=gc)
    app.show()
    qt_app.exec_()