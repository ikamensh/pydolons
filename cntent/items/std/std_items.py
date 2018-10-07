from cntent.items.materials.materials import Stones, Metals, Leathers
from cntent.items.blueprints.weapons import weapons as bp_weapons
from cntent.items.blueprints.armor import body_armor as bp_armor
from cntent.items.QualityLevels import QualityLevels

axe_ancient = bp_weapons.primordial_great_axe.to_item(Stones.flintstone, QualityLevels.SUPERIOR)

sword_cheap = bp_weapons.short_sword.to_item(Metals.bronze, QualityLevels.PRIMITIVE)
axe_cheap = bp_weapons.axe.to_item(Metals.bronze, QualityLevels.PRIMITIVE)
dagger_cheap = bp_weapons.dagger.to_item(Metals.bronze, QualityLevels.PRIMITIVE)
spear_cheap = bp_weapons.spear.to_item(Metals.bronze, QualityLevels.PRIMITIVE)
hammer_cheap = bp_weapons.hammer.to_item(Metals.bronze, QualityLevels.PRIMITIVE)


pirate_jacket = bp_armor.pirate_jacket.to_item(Leathers.skin, QualityLevels.PRIMITIVE)
hero_jacket = bp_armor.leather_outfit.to_item(Leathers.thick_skin, QualityLevels.SUPERIOR)
