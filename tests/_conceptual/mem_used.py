from DreamGame import DreamGame
from cntent.base_types.demo_hero import demohero_basetype
from cntent.dungeons.demo_dungeon_walls import walls_dungeon
from game_objects.battlefield_objects import Unit
import sys
import my_context

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

game = DreamGame.start_dungeon(walls_dungeon, Unit(demohero_basetype))
print(my_context.the_game is game)

sims = []
for i in range(1000):
    sims.append(game.simulation())


print(len(sims))

print( get_size(sims) )

print( get_size(game) )

print(my_context.the_game is game)