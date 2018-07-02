from content.dungeons.demo_dungeon import demo_dungeon
from DreamGame import DreamGame
from content.base_types.demo_hero import demohero_basetype
from game_objects.battlefield_objects.Unit.Unit import Unit

game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
print(game)
game.print_all_units()
game.loop(player_berserk=True)