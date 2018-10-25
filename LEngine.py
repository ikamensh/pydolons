from cntent.dungeons.demo_dungeon import demo_dungeon
from cntent.dungeons.demo_dungeon_walls import walls_dungeon
from cntent.dungeons.pirate_lair import pirate_lair
from cntent.dungeons.small_graveyard import small_graveyard
from cntent.dungeons.small_orc_cave import small_orc_cave

from mechanics.AI.SimGame import SimGame as DreamGame
from character_creation.Character import Character
from cntent.base_types.demo_hero import demohero_basetype

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
        self.game = None
        self.dungeon = None

    def getDungeon(self, levelName):
        """ В этом методе можно установить дополнительные условия для нужного подземелья
        """
        return self.dungeons[levelName]

    def getGame(self, levelName):
        if self.character is None or self.the_hero is None:
            self.character = Character(demohero_basetype)
            self.the_hero = self.character.unit
            self.dungeon = self.getDungeon(levelName)
            self.game = DreamGame.start_dungeon(self.dungeon, self.the_hero)
            self.game.character = self.character
            return  self.game
        else:
            self.dungeon = self.getDungeon(levelName)
            self.game = DreamGame.start_dungeon(self.getDungeon(levelName), self.the_hero)
            self.game.character = self.character
