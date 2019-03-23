import random


class RandomAI:
    def __init__(self, game, chance_pass = 0.):
        self.game = game
        self.battlefield = self.game.bf
        self.chance_pass = chance_pass


    def decide_step(self, active_unit):

        if self.chance_pass > random.random():
            return None, None

        assert active_unit in self.game.units

        actives = active_unit.actives

        targets = {}
        for a in actives:
            if a.affordable():
                tgts = self.game.get_possible_targets(a)
                if tgts:
                    targets[a] = tgts

        actives_with_valid_targets = set(targets.keys())
        actives_without_targeting = {a for a in actives if a.targeting_cls is None}

        active = random.choice( list(actives_with_valid_targets | actives_without_targeting) )
        if active in actives_without_targeting:
            return active, None
        else:
            target = random.choice(targets[active])
            return active, target




