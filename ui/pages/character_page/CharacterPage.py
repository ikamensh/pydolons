from __future__ import annotations
from ui.pages.AbstractPage import AbstractPage
from ui.pages.suwidgets.BaseItem import BaseItem
from ui.pages.suwidgets.TextItem import TextItem
from ui.pages.character_page.GamePerkTree import GamePerkTree
from ui.pages.character_page.GameMasteries import GameMasteries
from ui.pages.character_page.GameHeroAttr import GameHeroAttr
from PySide2 import QtCore

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages import GamePages


class CharacterPage(AbstractPage):
    def __init__(self, gamePages: GamePages):
        super().__init__(gamePages)
        self.readXML('character_page.xml')
        self.read_tree()
        self.gamePages.gameRoot.view.wheel_change.connect(self.updatePos)
        self.updatePos()
        self.name = 'character_page'
        self.input = ''
        character = self.gamePages.gameRoot.lengine.character
        self.setUpPerks(character)
        self.setUpMasteries(character)
        self.setUpHeroAttr(character)
        self.item_hover = None
        pass

    def keyPressEvent(self, e):
        pass

    def showPage(self):
        self.state = True
        self.gamePages.startPage.hidePage()
        self.show()

    def hidePage(self):
        self.state = False
        self.hide()

    def sceneEvent(self, event:QtCore.QEvent):
        if event.type() is QtCore.QEvent.GraphicsSceneMousePress:
            self.pressItem(self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform()))
            return True
        elif event.type() is QtCore.QEvent.GraphicsSceneMouseRelease:
            for item in self.pressed_buttons:
                item.isDown = False
                item.update()
            self.pressed_buttons.clear()
            self.releaseItem(self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform()))
            return True
        elif event.type() is QtCore.QEvent.GraphicsSceneHoverMove:
            self.hoverMove(self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform()))
            return True
        else:
            return super(CharacterPage, self).sceneEvent(event)

    def pressItem(self, item: BaseItem):
        if item is not None:
            if item.input == 'button':
                item.isDown = True
                self.pressed_buttons.append(item)
            item.update()

    def releaseItem(self, item: BaseItem):
        if item is not None:
            if item.input == 'button':
                if item._names[0] == 'perk':
                    self.perk_up(item._names[1])
                elif item._names[0] == 'mastery':
                    self.mastery_up(item._names[1])
                elif item._names[0] == 'cha':
                    self.heroAttr_change(item)
                elif item.name == 'button_accept_icon':
                    self.onClickAccept()
                elif item.name == 'button_deny_icon':
                    self.onClickDeny()
                elif item.name == 'button_close_icon':
                    self.onClickClose()

    def hoverItem(self, item):
        if item is not None:
            if item.input == 'button':
                if item._names[0] == 'perk':
                    # self.perk_up(item._names[1])
                    pass
                elif item._names[0] == 'mastery':
                    self.mastery_hover(item._names[1])

    def hoverMove(self, item):
        if item is not None:
            if item == self.item_hover:
                self.show_info(item)
                if item.input == 'button':
                    if item._names[0] == 'perk':
                        # self.perk_up(item._names[1])
                        pass
                    elif item._names[0] == 'mastery':
                        self.mastery_hover(item._names[1])
            else:
                self.clear_colors()
                self.item_hover = item

################################################
###########        P E R K S      ##############
################################################

    def setUpPerks(self, character):
        self.gpt = GamePerkTree(character.perk_trees[0], character)
        self.perk_all_update()

    def perk_up(self, name):
        perk = self.gpt.perks.get(name)
        if perk is not None and perk.current_level < 3:
            self.gpt.perk_up(perk)
            point = self.items.get(f'perk_{name}_point')
            if point is not None:
                point.setText(str(self.gpt.xp_to_text(perk)))
            level = self.items.get(f'perk_{name}_level')
            if level is not None:
                level.setText(f"Level {str(perk.current_level)}")
            spen_value = self.items.get('perk_spent_value')
            if spen_value is not None:
                spen_value.setText(self.gpt.spent_xp)
        self.heroAttr_all_update()
        self.mastery_all_update()
        self.perk_all_update()

    def perk_all_update(self):
        for name, perk in self.gpt.perks.items():
            point = self.items.get(f'perk_{name}_point')
            if point is not None:
                point.setText(str(self.gpt.xp_to_text(perk)))
            level = self.items.get(f'perk_{name}_level')
            if level is not None:
                level.setText(f"Level {str(perk.current_level)}")
        spen_value = self.items.get('perk_spent_value')
        if spen_value is not None:
            spen_value.setText(self.gpt.spent_xp)

################################################
###########   M A S T E R I E S   ##############
################################################

    def setUpMasteries(self, character):
        self.gm = GameMasteries(character)
        self.gm.setUpMasteries()
        self.mastery_bar_update()
        self.mastery_all_update()

    def mastery_up(self, name):
        mastery = self.gm.masteries.get(name)
        if mastery is not None:
            self.gm.mastery_up(mastery)
        self.mastery_all_update()
        self.update(0, 0, self.gamePages.gameRoot.cfg.dev_size[0], self.gamePages.gameRoot.cfg.dev_size[1])
        self.heroAttr_all_update()

    def mastery_hover(self, name):
        mastery = self.gm.masteries.get(name)
        if mastery is not None:
            perc, mm = self.gm.mastery_prec(mastery)
            for m in mm.keys():
                m_name = self.items.get(f'mastery_{m.name.lower()}_name')
                m_name.setColor('#FF4AFF')
                # self.update(0, 0, 1920, 1080)

    def mastery_bar_update(self):
        for name, mastery in self.gm.masteries.items():
            perc, __ = self.gm.mastery_prec(mastery)
            bar = self.items.get(f'mastery_{name}_bar')
            if bar is not None:
                bar._width = bar.width * perc

    def mastery_all_update(self):
        for name, mastery in self.gm.masteries.items():
            self.items.get(f'mastery_{name}_point').setText(self.gm.mastery_value(mastery))
            perc, __ = self.gm.mastery_prec(mastery)
            bar = self.items.get(f'mastery_{name}_bar')
            if bar is not None:
                bar._width = bar.width * perc
            spent_value = self.items.get('mastery_spent_value')
            if spent_value is not None:
                spent_value.setText(self.gm.spent_xp)

    ######################################
    #### H E R O  A T T R I B U T E S ####
    ######################################

    def setUpHeroAttr(self, character):
        self.gha = GameHeroAttr(character, self.gamePages.gameRoot)
        self.items.get('hero_icon').setPixmapIcon(self.gha.hero_icon)
        self.mastery_all_update()
        self.heroAttr_all_update()

    def heroAttr_all_update(self):
        for name, attr in self.gha.attrs.items():
            point = self.items.get(f'cha_{name}_point')
            if point is not None:
                point.setText(self.gha.attr_value(attr))
            xp_value = self.items.get('free_xp_value')
            if xp_value is not None:
                xp_value.setText(self.gha.free_xp)
            free_points_value = self.items.get('free_points_value')
            if free_points_value is not None:
                free_points_value.setText(self.gha.free_points)
        self.heroAttr_update()

    def heroAttr_change(self, item:BaseItem):
        if item._names[2] == 'up':
            self.heroAttr_up(item._names[1])
        elif item._names[2] == 'down':
            self.heroAttr_down(item._names[1])
        self.heroAttr_all_update()

    def heroAttr_up(self, name):
        heroAttr = self.gha.attrs.get(name)
        if heroAttr is not None:
            self.gha.attr_up(heroAttr)

    def heroAttr_down(self, name):
        heroAttr = self.gha.attrs.get(name)
        if heroAttr is not None:
            self.gha.attr_down(heroAttr)

    def heroAttr_update(self):
        self.items.get('attr_health_value').setText(self.gha.max_health + ' / ' + self.gha.health)
        self.items.get('attr_mana_value').setText(self.gha.max_mana + ' / ' + self.gha.mana)
        self.items.get('attr_stamina_value').setText(self.gha.max_stamina + ' / ' + self.gha.stamina)

        #####################
        ### B U T T O N S ###
        #####################

    def onClickAccept(self):
        self.gha.commit_changes()

    def onClickDeny(self):
        self.gha.reset_all()
        self.mastery_all_update()
        self.heroAttr_all_update()
        self.perk_all_update()

    def onClickClose(self):
        self.gha.reset_all()
        self.hidePage()
        self.gamePages.gameRoot.ui.startGame()
        self.gamePages.gameMenu.showPage()

        ###############
        ### I N F O ###
        ###############

    def show_info(self, item):
        info = self.gpt.perks_info.get(item.name)
        if info is None:
            info = self.gm.masteries_info.get(item.name)
        if info is None:
            info = self.gha.attrs_info.get(item.name)
        if info is not None:
            self.items.get('info_value').setText(self.setDict(info))
        pass

    def clear_colors(self):
        for item in self.items.values():
            if isinstance(item, TextItem):
                item.setColor(item._color)




