from mechanics.flexi_targeting import EffectPack, PackTargeting
from content.effects.AttackEffect import AttackEffect

attack_unit_event = EffectPack([AttackEffect], PackTargeting.TARGET_UNIT)
attack_cell_event = EffectPack([AttackEffect], PackTargeting.UNIT_ON_TARGET_CELL)