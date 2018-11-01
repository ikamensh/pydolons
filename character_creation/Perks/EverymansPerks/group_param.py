from mechanics.buffs import Ability
#TODO packaging makes no sense?
from game_objects.battlefield_objects.CharAttributes import CharAttributes as ca, Constants as c
from game_objects.attributes import Bonus, Attribute
from character_creation.Perks import Perk
from character_creation.Perks import PerkGroup

from character_creation.Perks.EverymansPerks.group_attrib import pg_attributes



def param_bonus_abilities(attr, base, bonus, multi):
    b1 = Bonus({attr: Attribute(base, multi, bonus)})
    b2 = Bonus({attr: Attribute(base*2, multi*2.25, bonus*2)})
    b3 = Bonus({attr: Attribute(base*3, multi*4, bonus*4)})

    a1 = Ability(b1)
    a2 = Ability(b2)
    a3 = Ability(b3)

    return {1:a1, 2:a2, 3:a3}

health_perk = Perk("Incredible Health", param_bonus_abilities(ca.HEALTH, 1*c.HP_PER_STR, 20, 2*c.HP_PER_STR))

mana_perk = Perk("Incredible Mana", param_bonus_abilities(ca.MANA, 2*c.MANA_PER_INT, 30, 2*c.MANA_PER_INT))

stamina_perk = Perk("Incredible Stamina", param_bonus_abilities(ca.STAMINA, 2*c.STAMINA_PER_END, 30,
                                                          2*c.STAMINA_PER_END))

ini_perk = Perk("Incredible Initiative", param_bonus_abilities(ca.INITIATIVE, 0.3, 7, 0.3))




pg_params = PerkGroup([health_perk, mana_perk, stamina_perk, ini_perk], requirements={pg_attributes:2})

