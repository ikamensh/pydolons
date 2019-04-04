from __future__ import annotations

from DreamGame import DreamGame
# from GameImitation import DreamGame
from character.Character import Character
from cntent.base_types.demo_hero import demohero_basetype

# import triggers
from ui.gamecore.triggers.animation_triggers import move_anim_trigger, damage_anim_trigger, attack_anin_trigger, \
    perish_anim_trigger, turn_anim_trigger, nexunit_anim_trigger, levelstatus_trigger, ui_error_message_trigger, \
    obstacle_destroy_trigger

from single_player.Shop import Shop, generate_assortment, all_blueprints, all_materials, QualityLevels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit
    from game_objects.dungeon.Dungeon import Dungeon


class LEngine:
    """
    LogicEngine
    """
    def __init__(self):
        self.character: Character = None
        self.the_hero: Unit = None
        self.dungeon: Dungeon = None

    def getHero(self):
        if self.character is None:
            self.character = Character(demohero_basetype)
        elif self.the_hero is None:
            self.character = Character(demohero_basetype)
        return self.character.unit

    def getGame(self):
        if self.dungeon is None:
            print('Not select dungeon')
        self.the_hero = self.getHero()
        return self._getGame(self.dungeon)

    def _getGame(self, dungeon):
        print('Start dungeon:', dungeon.name)
        game = DreamGame.start_dungeon(dungeon, self.the_hero)
        self.setUpTriggers(game)
        game.character = self.character
        game.shop = self.getShop(single_palyer=True)
        return game

    def setUpTriggers(self, game):
        levelstatus_trigger(game),
        ui_error_message_trigger(game),
        nexunit_anim_trigger(game),
        turn_anim_trigger(game),
        perish_anim_trigger(game),
        attack_anin_trigger(game),
        damage_anim_trigger(game),
        move_anim_trigger(game),
        obstacle_destroy_trigger(game)

    def getShop(self, single_palyer = True):
        shop = None
        if single_palyer and self.character is not None:
            return Shop(generate_assortment(all_blueprints, all_materials, QualityLevels.all),
                        1, 500, customer=self.character)
        return shop

