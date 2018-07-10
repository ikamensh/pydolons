import inspect
from mechanics.events.EventsPlatform import EventsPlatform

class Trigger:
    def __init__(self, target_event_cls, conditions,
                 source = None, effect_trigger_pack = None):
        assert inspect.isclass(target_event_cls)
        assert isinstance(conditions, dict)
        self.target_event_cls = target_event_cls
        self.conditions = conditions
        assert (effect_trigger_pack is None) == (source is None)
        self.effect_pack = effect_trigger_pack
        self.source = source
        EventsPlatform.triggers.add(self)

    def check_conditions(self, event):
        assert isinstance(event, self.target_event_cls)
        for key, value in self.conditions.items():
            if getattr(event, key) != value:
                return False

        return True

    def try_on_event(self, event):
        if self.check_conditions(event):
            self.effect_pack.resolve(self.source, event)

    def deactivate(self):
        EventsPlatform.triggers.remove(self)




