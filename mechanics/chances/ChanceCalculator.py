class ChanceCalculator:
    advantage_to_double = 25

    @staticmethod
    def chance(base_prob, precision, evasion):
        assert 0 <= base_prob <= 1
        if base_prob == 0 or base_prob == 1:
            return base_prob

        if precision == evasion:
            return base_prob

        if evasion > precision:
            adv = 1 + (evasion - precision) / ChanceCalculator.advantage_to_double
        else:
            adv = 1 / (1 + (precision - evasion) / ChanceCalculator.advantage_to_double)


        if base_prob >= 0.5:
            new_chance = base_prob ** adv    # Note: as base_prob is below one, powers below one increase the

        else:
            chance_to_avoid = 1 - base_prob
            adv = 1/adv
            new_chance_to_avoid = chance_to_avoid ** adv
            new_chance = 1 - new_chance_to_avoid


        assert 0 <= new_chance <= 1
        return new_chance



if __name__ == "__main__":

    for base_chance in [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]:
        for attack, defense in [(0,25), (25,0), (75,0), (0, 75) , (225,0), (0, 225)]:
            if defense > attack:
                adv = 1 + (defense - attack) / ChanceCalculator.advantage_to_double
            else:
                adv = 1 / (1 + (attack - defense) / ChanceCalculator.advantage_to_double)
            print(base_chance, attack, defense, adv, ChanceCalculator.chance(base_chance, attack, defense))