class EffectPack:
    def __init__(self, targeted_effects):
        self.targeted_effects = targeted_effects

    def resolve(self, source, user_targeting):
        for effect, targeting_factory in self.targeted_effects:
            targets = targeting_factory(user_targeting)

            if targets:
                try:
                    for target in targets:
                        effect.apply(source, target)
                except TypeError:
                    effect.apply(source, targets)


