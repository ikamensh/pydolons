from character_creation.Character import Character
from mechanics.AI.SimGame import SimGame as DreamGame
from cntent.base_types.demo_hero import demohero_basetype
from cntent.dungeons.demo_dungeon import demo_dungeon

class levels:
    default ="demo_dungeon"

def one_game():
    character  = Character(demohero_basetype)
    game = DreamGame.start_dungeon(demo_dungeon, character.unit)
    game.character = character
    game.print_all_units()
    game.loop()


if __name__ == "__main__":
    one_game()

