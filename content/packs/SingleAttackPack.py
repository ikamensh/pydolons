from mechanics.flexi_targeting import EffectPack
from content.effects.SingleAttack import AttackEffect
from content.targeting_factory.targeting_factory import cell_to_unit, same_unit_as_targeted

attack_unit_pack = EffectPack([(AttackEffect, same_unit_as_targeted)])
attack_cell_pack = EffectPack([(AttackEffect, cell_to_unit)])