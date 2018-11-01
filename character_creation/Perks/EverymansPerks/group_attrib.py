from mechanics.buffs import Ability
#TODO packaging makes no sense?
from game_objects.battlefield_objects import CharAttributes
from game_objects.attributes import Bonus, Attribute
from character_creation.Perks import Perk
from character_creation.Perks import PerkGroup

def attr_bonus_abilities(attr):
    b1 = Bonus({attr: Attribute(1, 10, 1)})
    b2 = Bonus({attr: Attribute(2, 20, 2)})
    b3 = Bonus({attr: Attribute(3, 35, 4)})

    a1 = Ability(b1)
    a2 = Ability(b2)
    a3 = Ability(b3)

    return {1:a1, 2:a2, 3:a3}




str_perk = Perk("Gifted: Streingth", attr_bonus_abilities(CharAttributes.STREINGTH))
agi_perk = Perk("Gifted: Agility", attr_bonus_abilities(CharAttributes.AGILITY))
end_perk = Perk("Gifted: Endurance", attr_bonus_abilities(CharAttributes.ENDURANCE))

prc_perk = Perk("Gifted: Perception", attr_bonus_abilities(CharAttributes.PERCEPTION))
int_perk = Perk("Gifted: Intelligence", attr_bonus_abilities(CharAttributes.INTELLIGENCE))
cha_perk = Perk("Gifted: Charisma", attr_bonus_abilities(CharAttributes.CHARISMA))


pg_attributes = PerkGroup([str_perk, agi_perk, end_perk, prc_perk, int_perk, cha_perk])