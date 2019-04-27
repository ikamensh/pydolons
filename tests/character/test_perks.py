

def test_works_on_character(char_with_xp):
    char = char_with_xp
    ep = char.perk_trees[0]
    str_perk = ep.accessible_perks()[0]

    str_before = char.unit.str
    exp_before = char.free_xp

    ep.perk_up(str_perk)
    char.update_unit()

    assert char.unit.str > str_before
    assert char.free_xp < exp_before


def test_reset_perks(char_with_xp):
    char = char_with_xp
    ep = char.perk_trees[0]
    str_perk = ep.accessible_perks()[0]

    str_before = char.unit.str
    exp_before = char.free_xp

    ep.perk_up(str_perk)
    char.update_unit()
    char.reset_perks()
    char.update_unit()

    assert char.unit.str == str_before
    assert char.free_xp == exp_before


def test_reset(char_with_xp):
    char = char_with_xp
    ep = char.perk_trees[0]
    str_perk = ep.accessible_perks()[0]

    str_before = char.unit.str
    exp_before = char.free_xp

    ep.perk_up(str_perk)
    char.update_unit()
    char.reset()

    assert char.unit.str == str_before
    assert char.free_xp == exp_before

def test_commit(char_with_xp):
    char = char_with_xp
    ep = char.perk_trees[0]
    str_perk = ep.accessible_perks()[0]

    str_before = char.unit.str
    exp_before = char.free_xp

    ep.perk_up(str_perk)
    char.update_unit()

    char.commit()
    char.reset()

    assert char.unit.str > str_before
    assert char.free_xp < exp_before