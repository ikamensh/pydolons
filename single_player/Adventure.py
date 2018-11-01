from character.Character import Character
from mechanics.AI.SimGame import SimGame
from game_objects.battlefield_objects import Unit
from single_player.Shop import Shop


class Adventure:
    def __init__(self, base_type, first_mission):
        self.character = Character(base_type)
        self.first_mission = first_mission

    def start(self):
        for dungeon in self.first_mission:
            hero_unit = self.character.unit
            game = SimGame.start_dungeon(dungeon, hero_unit)
            result = game.loop()
            if result != "VICTORY":
                print("you have lost the game.")
                return "DEFEAT"
            self.character.update(hero_unit)

        return "VICTORY"





