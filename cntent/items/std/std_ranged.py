from cntent.items.materials.materials import Woods
from cntent.items.blueprints.weapons import weapons as bp_weapons
from cntent.items.QualityLevels import QualityLevels


black_bow = bp_weapons.bow.to_item(Woods.black_wood, QualityLevels.USUAL)
cheap_bow = bp_weapons.bow.to_item(Woods.oak, QualityLevels.CRUDE)

cadamba_crossbow = bp_weapons.crossbow.to_item(Woods.cadamba_tree, QualityLevels.USUAL)
quality_crossbow = bp_weapons.crossbow.to_item(Woods.wood, QualityLevels.MASTERPIECE)



