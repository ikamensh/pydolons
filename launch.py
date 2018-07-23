from DreamGame import DreamGame
from content.base_types.demo_hero import demohero_basetype
from content.dungeons.demo_dungeon import demo_dungeon
from game_objects.battlefield_objects import Unit

game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
print(game)
game.print_all_units()
hero_turns = game.loop(player_berserk=True)
print("hero has made {} turns.".format(hero_turns))