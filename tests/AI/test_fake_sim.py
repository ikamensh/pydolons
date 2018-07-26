
def test_results_match(game, hero):

    count_simulated = 0

    choices = game.get_all_choices(hero)
    fraction = game.fractions[hero]

    for c in choices:
        active, target = c
        if active.simulate_callback:
            count_simulated += 1
            fake_util = game.fake_measure(c, fraction)
            sim = game.step_into_sim(active, target)
            real_util = sim.utility(fraction)
            assert fake_util == real_util


    assert count_simulated > 0


