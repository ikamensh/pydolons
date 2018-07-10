import inspect

class Trigger:
    def __init__(self, target_event_cls, conditions, effect_pack = None, targeting_constructor = None):
        assert inspect.isclass(target_event_cls)
        assert isinstance(conditions, dict)
        self.target_event_cls = target_event_cls
        self.conditions = conditions
        assert effect_pack is None == targeting_constructor is None
        self.effect_pack = effect_pack
        self.targeting_constructor = targeting_constructor

    def check_conditions(self, event):
        assert isinstance(event, self.target_event_cls)
        for key, value in self.conditions:
            if getattr(event, key) != value:
                return False

        return True

    def activate(self, event):
        if self.effect_pack:
            targeting = self.targeting_constructor(event)
            self.effect_pack.resolve(targeting)

    def try_on_event(self, event):
        if self.check_conditions(event):
            self.activate(event)




