from __future__ import annotations

from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLayout
from ui.GamePages.suwidgets.perk_tree.QPerk import QPerk

from character.perks import PerkGroup
# from ui.GamePages.suwidgets.perk_tree.QPerkTree import QPerkTree

import math

class QPerkGroup(QWidget):
    def __init__(self, cfg, perk_group: PerkGroup, parent):
        self.cfg = cfg
        self.perk_group = perk_group
        self.tree = parent
        super().__init__(parent)

        layout = QVBoxLayout()

        layout.setSizeConstraint(QLayout.SetFixedSize)

        n_perks = len( perk_group.perk_list )
        n_per_row = math.ceil( n_perks ** (1/2) )
        n_rows = math.ceil(n_perks / n_per_row)

        self.identities = {}
        for i in range(n_rows):
            start = i*n_per_row
            finish = start + n_per_row
            row, new_identities = self.build_row( perk_group.perk_list[start:finish] )
            self.identities.update(new_identities)
            layout.addWidget(row)

        self.setLayout(layout)


    def xp_changed(self, new_xp):
        can_spend = new_xp
        if not self.perk_group.requirements_matched():
            can_spend = 0

        for qperk in self.identities.values():
            qperk.xp_changed(can_spend)

    def levelup(self):
        self.tree.levelup()


    def build_row(self, perks):
        row = QWidget(self)
        layout = QHBoxLayout()

        identities = {}

        for perk in perks:

            qperk = QPerk(self.cfg, perk, self)
            identities[perk] = qperk
            layout.addWidget(qperk)

        row.setLayout(layout)
        return row, identities

    def __repr__(self):
        return f"UI for {self.perk_group}"





if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    from character.perks.everymans_perks.group_attrib import pg_attributes

    qt_app = QApplication()

    app = QPerkGroup(pg_attributes)
    app.show()

    qt_app.exec_()