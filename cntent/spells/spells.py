from cntent.spells.concepts import lightning_concept, heal_concept
from cntent.spells import runes
from mechanics.actives import Active

spell = lightning_concept.to_spell([runes.double_damage_rune])
lightning_active = Active.from_spell(spell)


spell = heal_concept.to_spell([runes.double_damage_rune])
heal_active = Active.from_spell(spell)
