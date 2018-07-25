

def test_more_hp_is_better(game, hero):

    utility_initial = game.utility(game.fractions[hero])
    assert hero in game.units

    hero.max_health += 100

    assert utility_initial < game.utility(game.fractions[hero])

def test_invertion(game, hero, pirate):

    utility_initial = game.utility(game.fractions[pirate])

    hero.max_health += 100

    assert utility_initial > game.utility(game.fractions[pirate])


def test_more_mana_is_better(game, hero):
    utility_initial = game.utility(game.fractions[hero])

    hero.max_mana += 100

    assert utility_initial < game.utility(game.fractions[hero])


def test_more_stamina_is_better(game, hero):
    utility_initial = game.utility(game.fractions[hero])

    hero.max_stamina += 100

    assert utility_initial < game.utility(game.fractions[hero])


def test_more_readiness_is_better(game, hero):
    utility_initial = game.utility(game.fractions[hero])

    hero.readiness += 100

    assert utility_initial < game.utility(game.fractions[hero])