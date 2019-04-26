from character import Character, MasteriesEnum


def test_can_up_all_masteries(demohero_basetype):
    c = Character(demohero_basetype)
    c.unit.xp = int(1e100)
    assert set(c.masteries_can_go_up) == set(MasteriesEnum)

def test_can_up_a_lot(char, one_mastery):
    char.unit.xp = int(1e100)

    last_cost = 0
    delta_exp_before = 0
    for i in range(200):
        mastery_before = char.masteries[one_mastery]
        exp_before = char.free_xp

        char.increase_mastery(one_mastery)
        delta_exp = exp_before - char.free_xp
        assert char.unit.masteries[one_mastery] > mastery_before
        assert last_cost < char.unit.masteries.calculate_cost(one_mastery)[0] # cost grows
        assert delta_exp > delta_exp_before
        last_cost = char.masteries.calculate_cost(one_mastery)[0]
        delta_exp_before = delta_exp




def test_reset_mastery(char, one_mastery):
    char.unit.xp = int(1e100)
    exp_initially = char.free_xp
    lvl_initially = char.masteries[one_mastery]

    for i in range(1):
        char.increase_mastery(one_mastery)

    assert char.free_xp < exp_initially
    assert char.unit.masteries[one_mastery] > lvl_initially

    char.reset()

    assert char.masteries[one_mastery] == lvl_initially
    assert char.unit.masteries[one_mastery] == lvl_initially
    assert char.free_xp == exp_initially





def test_up_mastery(demohero_basetype, var_mastery):
    c = Character(demohero_basetype)
    mastery_before = c.masteries[var_mastery]

    c.increase_mastery(var_mastery)

    assert c.unit.masteries[var_mastery] > mastery_before




