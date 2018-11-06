from cntent.dungeons.demo_dungeon import demo_dungeon
from cntent.dungeons.demo_dungeon_walls import walls_dungeon
from cntent.dungeons.pirate_lair import pirate_lair
from cntent.dungeons.small_graveyard import small_graveyard
from cntent.dungeons.small_orc_cave import small_orc_cave

from mechanics.AI.SimGame import SimGame
# from GameImitation import DreamGame
from character.Character import Character
from cntent.base_types.demo_hero import demohero_basetype

# import triggers
from ui.triggers.animation_triggers import move_anim_trigger, damage_anim_trigger, attack_anin_trigger, \
    perish_anim_trigger, turn_anim_trigger, nexunit_anim_trigger, levelstatus_trigger, ui_error_message_trigger

class LEngine:
    """
    LogicEngine
    """
    def __init__(self):
        self.dungeons = {}
        self.dungeons['demo_level'] = demo_dungeon
        self.dungeons['walls_level'] = walls_dungeon
        self.dungeons['pirate_level'] = pirate_lair
        self.dungeons['small_graveyard_level'] = small_graveyard
        self.dungeons['small_orc_cave_level'] = small_orc_cave
        self.character:Character = None
        self.the_hero  = None
        self.dungeon = None

    def getDungeon(self, levelName):
        """ В этом методе можно установить дополнительные условия для нужного подземелья
        """
        return self.dungeons[levelName]

    def getGame(self, levelName):
        if self.character is None or self.the_hero is None:
            self.character = Character(demohero_basetype)
            self.the_hero = self.character.unit
            game = self._getGame(levelName)
            return  game
        else:
            return self._getGame(levelName)

    def _getGame(self, levelName):
        game = SimGame.start_dungeon(self.getDungeon(levelName), self.the_hero)
        self.setUpTriggers(game)
        game.character = self.character
        return game


    def setUpTriggers(self, game):
        levelstatus_trigger(game),
        ui_error_message_trigger(game),
        nexunit_anim_trigger(game),
        turn_anim_trigger(game),
        perish_anim_trigger(game),
        attack_anin_trigger(game),
        damage_anim_trigger(game),
        move_anim_trigger(game)

