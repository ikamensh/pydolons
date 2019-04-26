def test_works_on_character(char):
    ep = char.perk_trees[0]
    str_perk = ep.accessible_perks()[0]

    str_before = char.unit.str

    str_perk.current_level +=3
    char.update_unit()

    assert char.unit.str > str_before