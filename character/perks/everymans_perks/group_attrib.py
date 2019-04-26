from game_objects.battlefield_objects import CharAttributes, enum_to_abbrev
from game_objects.attributes import Bonus, Attribute
from character.perks import Perk
from character.perks import PerkGroup

def attr_bonus_abilities(attr):
    from mechanics.buffs import Ability
    b1 = Bonus({attr: Attribute(1, 10, 1)})
    b2 = Bonus({attr: Attribute(2, 20, 2)})
    b3 = Bonus({attr: Attribute(3, 35, 4)})

    a1 = Ability(b1)
    a2 = Ability(b2)
    a3 = Ability(b3)

    return {1:a1, 2:a2, 3:a3}

def attr_perk_names(attr):
    fmt = "Gifted: {}"
    return {
            1:fmt.format(str(attr) +" I"),
            2: fmt.format(str(attr) + " II"),
            3: fmt.format(str(attr) + " III")}

def build_perk(attr):
    return Perk(attr_perk_names(attr), attr_bonus_abilities(attr),
                # icon=os.path.join("icons", "params", "64", enum_to_abbrev[attr]) +".png" )
                icon=enum_to_abbrev[attr] +".png")


str_perk = build_perk(CharAttributes.STREINGTH)
agi_perk = build_perk(CharAttributes.AGILITY)
end_perk = build_perk(CharAttributes.ENDURANCE)

prc_perk = build_perk(CharAttributes.PERCEPTION)
int_perk = build_perk(CharAttributes.INTELLIGENCE)
cha_perk = build_perk(CharAttributes.CHARISMA)


pg_attributes = PerkGroup([str_perk, agi_perk, end_perk, prc_perk, int_perk, cha_perk])