import copy
from character.perks.everymans_perks.everymans_perk_tree import everymans_perks


def test_cost_grows():
    ep = everymans_perks()

    str_perk = ep.accessible_perks()[0]
    agi_perk = ep.accessible_perks()[1]

    cost_str = ep.cost_to_levelup(str_perk)
    cost_agi = ep.cost_to_levelup(agi_perk)

    str_perk.current_level += 1

    assert cost_str < ep.cost_to_levelup(str_perk)
    assert cost_agi < ep.cost_to_levelup(agi_perk)

    assert ep.cost_to_levelup(agi_perk) < ep.cost_to_levelup(str_perk)


def test_gives_abilities():
    ep = everymans_perks()

    assert len(ep.all_abils) == 0

    str_perk = ep.accessible_perks()[0]
    agi_perk = ep.accessible_perks()[1]

    str_perk.current_level += 1

    assert len(ep.all_abils) == 1

    str_perk.current_level += 1

    assert len(ep.all_abils) == 1

    agi_perk.current_level += 1

    assert len(ep.all_abils) == 2


def test_gives_bonuses(hero):
    ep = everymans_perks()

    hero2 = copy.copy(hero)

    str_before = hero.str

    str_perk = ep.accessible_perks()[0]
    str_perk.current_level += 1

    for a in ep.all_abils:
        hero.add_ability(a)

    assert hero.str > str_before

    str_perk.current_level += 1

    for a in ep.all_abils:
        hero2.add_ability(a)

    assert hero2.str > hero.str


def test_works_on_character(char):
    ep = char.perk_trees[0]
    str_perk = ep.accessible_perks()[0]

    str_before = char.unit.str

    str_perk.current_level += 3

    assert char.unit.str > str_before


def test_stable_on_character(char):
    ep = char.perk_trees[0]
    str_perk = ep.accessible_perks()[0]

    str_perk.current_level += 3

    str_before = char.unit.str

    assert char.unit.str == str_before
