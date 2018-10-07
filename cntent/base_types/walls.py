from game_objects.battlefield_objects import Obstacle
from mechanics.damage import DamageTypeGroups


resists = {x:-0.6 for x in DamageTypeGroups.physical}
resists.update({x:0.75 for x in DamageTypeGroups.elemental})

mud_wall = lambda : Obstacle("Wall of mud", 5000, armor=50, resists=resists, icon="wall.png")