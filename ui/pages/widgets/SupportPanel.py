from __future__ import annotations

from PySide2.QtWidgets import QWidget, QVBoxLayout
from ui.pages.widgets.GameButton import GameButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages import AbstractPage
    from ui.core.gameconfig.GameConfiguration import GameConfiguration


class SupportPanel(QWidget):
    def __init__(self, page, gameconfig, parent=None):
        super(SupportPanel, self).__init__(parent)
        self.page: AbstractPage = page
        self.cfg: GameConfiguration = gameconfig
        self.w = 84 * self.cfg.scale_x
        self.h = self.w * 2
        self.setFixedSize(self.w, self.h)
        self.widget_x = self.cfg.dev_size[0] - self.w
        self.widget_y = 0
        self.setUpStyles()

    def setUpStyles(self):
        pic_path = self.cfg.pic_file_paths.get('scroll_background.png')
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0);')
        # if pic_path:
        #     self.setStyleSheet("background-image: url('" + pic_path + "');")
        bg_style = '''background-repeat: no-repeat;
        '''
        self.up_chest = None
        self.down_chest = None
        pic_path = self.cfg.pic_file_paths.get('chest_0.png')
        if pic_path:
            self.down_chest = "background-image: url('" + pic_path + "');"+bg_style
        pic_path = self.cfg.pic_file_paths.get('chest_1.png')
        if pic_path:
            self.up_chest = "background-image: url('" + pic_path + "');"+bg_style

        pic_path = self.cfg.pic_file_paths.get('navigation.png')
        self.navigation = "background-image: url('" + pic_path + "');"+bg_style

    def setUpWidgets(self):
        layout = QVBoxLayout(self)
        layout.setMargin(4)
        button = GameButton(parent=self)
        button.hovered.connect(self.up_chest_btn)
        button.hover_out.connect(self.down_chest_btn)
        button.clicked.connect(self.pressInventary)
        if self.down_chest:
            button.setStyleSheet(self.down_chest)
        w = 66 * self.cfg.scale_x
        button.setFixedSize(w, w)
        layout.addWidget(button)

        button = GameButton(parent=self)
        button.setStyleSheet(self.navigation)
        button.clicked.connect(self.pressNavigation)
        w = 67 * self.cfg.scale_x
        button.setFixedSize(w, w)
        layout.addWidget(button)
        self.setLayout(layout)

    def up_chest_btn(self, btn):
        if self.up_chest:
            btn.setStyleSheet(self.up_chest)

    def down_chest_btn(self, btn):
        if self.down_chest:
            btn.setStyleSheet(self.down_chest)

    def pressInventary(self):
        self.page.gamePages.pages['inventoryPage'].showPage()

    def pressNavigation(self):
        self.page.gamePages.gameRoot.controller.tr_support.setMovableMaps()
