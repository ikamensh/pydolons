from game_objects.battlefield_objects.Unit.BaseType import BaseType
from mechanics.damage import DamageTypeGroups

resists = {x:0.6 for x in DamageTypeGroups.physical}
resists.update({x:-0.5 for x in DamageTypeGroups.elemental})

mud_golem_basetype = BaseType({'str':17, 'agi':4, 'int':0}, "Mud Golem", resists=resists, icon="golem.png")