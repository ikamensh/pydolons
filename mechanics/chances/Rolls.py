from mechanics.chances import ChanceCalculator


def roll(base_a, bet_a, bet_b, random):
    chance_a = ChanceCalculator.chance(base_a, bet_a, bet_b)
    return random.random() < chance_a
