from content.items.materials.materials import Stones, Metals, Leathers
from content.items.blueprints.weapons import weapons as bp_weapons
from content.items.blueprints.armor import body_armor as bp_armor
from content.items.QualityLevels import QualityLevels

ancient_axe = bp_weapons.primordial_great_axe.to_item(Stones.flintstone, QualityLevels.SUPERIOR)
cheap_sword = bp_weapons.short_sword.to_item(Metals.bronze, QualityLevels.PRIMITIVE)

pirate_jacket = bp_armor.pirate_jacket.to_item(Leathers.skin, QualityLevels.PRIMITIVE)
hero_jacket = bp_armor.leather_outfit.to_item(Leathers.thick_skin, QualityLevels.SUPERIOR)
