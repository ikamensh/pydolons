from content.effects.FireDamage50 import FireDamage50
from content.triggers.event_to_targeting.target_attacker import target_attacker
from mechanics.flexi_targeting import EffectPack


fire_damage_to_attacker = EffectPack([(FireDamage50, target_attacker)])