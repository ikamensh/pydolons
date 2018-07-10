class EffectPack:
    def __init__(self, targeted_effects):
        self.targeted_effects = targeted_effects

    def resolve(self, source, targeting_info):
        """
        :param source: the unit who is author of the effects
        :param targeting_info: either an event (Triggers) or user_targeting (Actives)
        :return: 
        """
        for effect, targeting_factory in self.targeted_effects:
            targets = targeting_factory(targeting_info)

            if targets:
                try:
                    for target in targets:
                        effect.apply(source, target)
                except TypeError:
                    effect.apply(source, targets)


