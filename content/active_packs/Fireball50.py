from content.effects.FireDamage50 import FireDamage50
from content.targeting_factory.targeting_factory import all_in_aoe_around_cell
from mechanics.flexi_targeting import EffectPack


fireball_pack = EffectPack( [(FireDamage50, all_in_aoe_around_cell(2))] )