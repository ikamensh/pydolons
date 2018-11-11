from mechanics.buffs import Ability
#TODO packaging makes no sense?
from game_objects.battlefield_objects.CharAttributes import CharAttributes as ca, Constants as c
from game_objects.attributes import Bonus, Attribute
from character.perks import Perk
from character.perks import PerkGroup

from character.perks.everymans_perks.group_attrib import pg_attributes



def param_bonus_abilities(attr, base, bonus, multi):
    b1 = Bonus({attr: Attribute(base, multi, bonus)})
    b2 = Bonus({attr: Attribute(base*2, multi*2.25, bonus*2)})
    b3 = Bonus({attr: Attribute(base*3, multi*4, bonus*4)})

    a1 = Ability(b1)
    a2 = Ability(b2)
    a3 = Ability(b3)

    return {1:a1, 2:a2, 3:a3}

def attr_perk_names(attr):
    fmt1 = "Unusual {}"
    fmt2 = "Superior {}"
    fmt3 = "Incredible {}"

    return {
            1:fmt1.format(str(attr) +" I"),
            2: fmt2.format(str(attr) + " II"),
            3: fmt3.format(str(attr) + " III")}

health_perk = Perk(attr_perk_names(ca.HEALTH), param_bonus_abilities(ca.HEALTH, 1*c.HP_PER_STR, 20, 2*c.HP_PER_STR), cost_factor=2.5)

mana_perk = Perk(attr_perk_names(ca.MANA), param_bonus_abilities(ca.MANA, 2*c.MANA_PER_INT, 30, 2*c.MANA_PER_INT), cost_factor=2.5)

stamina_perk = Perk(attr_perk_names(ca.STAMINA), param_bonus_abilities(ca.STAMINA, 2*c.STAMINA_PER_END, 30,
                                                          2*c.STAMINA_PER_END), cost_factor=2.5)

ini_perk = Perk(attr_perk_names(ca.INITIATIVE), param_bonus_abilities(ca.INITIATIVE, 0.3, 7, 0.3), cost_factor=2.5)




pg_params = PerkGroup([health_perk, mana_perk, stamina_perk, ini_perk], requirements={pg_attributes:2})

