from character import Character, MasteriesEnum


def test_can_up_all_masteries(demohero_basetype):
    c = Character(demohero_basetype)
    c.unit.xp = int(1e100)
    assert set(c.masteries_can_go_up) == set(MasteriesEnum)

def test_can_up_a_lot(char, some_mastery):
    char.unit.xp = int(1e100)

    delta_exp_before = 0

    for i in range(20):
        mastery_before = char.masteries[some_mastery]
        exp_before = char.free_xp

        char.increase_mastery(some_mastery)
        delta_exp = exp_before - char.free_xp
        assert char.unit.masteries[some_mastery] > mastery_before
        assert delta_exp > delta_exp_before
        delta_exp_before = delta_exp

    char.temp_masteries.exp_spent[some_mastery] = char.masteries.cumulative_cost(300)
    char.update_unit()
    delta_exp_before = 0

    for i in range(300, 320):
        mastery_before = char.masteries[some_mastery]
        exp_before = char.free_xp

        char.increase_mastery(some_mastery)
        delta_exp = exp_before - char.free_xp
        assert char.unit.masteries[some_mastery] > mastery_before
        assert delta_exp > delta_exp_before
        delta_exp_before = delta_exp




def test_reset_mastery(char, some_mastery):
    char.unit.xp = int(1e100)
    exp_initially = char.free_xp
    lvl_initially = char.masteries[some_mastery]

    for i in range(1):
        char.increase_mastery(some_mastery)

    assert char.free_xp < exp_initially
    assert char.unit.masteries[some_mastery] > lvl_initially

    char.reset()

    assert char.masteries[some_mastery] == lvl_initially
    assert char.unit.masteries[some_mastery] == lvl_initially
    assert char.free_xp == exp_initially


def test_commit_mastery(char, some_mastery):
    char.unit.xp = int(1e100)
    exp_initially = char.free_xp
    lvl_initially = char.masteries[some_mastery]

    for i in range(1):
        char.increase_mastery(some_mastery)

    assert char.free_xp < exp_initially
    assert char.unit.masteries[some_mastery] > lvl_initially

    char.commit()
    char.reset()

    assert char.masteries[some_mastery] > lvl_initially
    assert char.unit.masteries[some_mastery] > lvl_initially
    assert char.free_xp < exp_initially


def test_up_mastery(demohero_basetype, var_mastery):
    c = Character(demohero_basetype)
    mastery_before = c.masteries[var_mastery]

    c.increase_mastery(var_mastery)

    assert c.unit.masteries[var_mastery] > mastery_before


def test_no_xp_cant_up(char, some_mastery):
    char.unit.xp = 0
    assert set(char.masteries_can_go_up) == set()





