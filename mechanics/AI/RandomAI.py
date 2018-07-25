import random
import my_context

#TODO consider using the context game.
class RandomAI:
    def __init__(self, game):
        self.game = game
        self.battlefield = self.game.battlefield


    def decide_step(self, active_unit):

        assert active_unit in self.battlefield.unit_locations

        actives = active_unit.actives

        targets = {}
        for a in actives:
            if a.owner_can_afford_activation():
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




