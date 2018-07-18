from game_objects.battlefield_objects.Unit.BaseType import BaseType
from mechanics.damage import DamageTypeGroups


resists = {x:-0.6 for x in DamageTypeGroups.physical}
resists.update({x:0.75 for x in DamageTypeGroups.elemental})

mud_wall_type = BaseType({'str':100}, "Wall of mud", resists=resists, armor_base=50, icon="wall.png")