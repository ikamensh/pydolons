import inspect
import my_context

class Trigger:
    def __init__(self, target_event_cls, conditions, source = None,
                 effect_trigger_pack = None, is_interrupt = False, event_callbacks=None):

        assert inspect.isclass(target_event_cls)
        assert isinstance(conditions, dict)
        self.target_event_cls = target_event_cls
        self.conditions = conditions
        self.effect_pack = effect_trigger_pack
        self.source = source
        self.is_interrupt = is_interrupt
        self.event_callbacks = event_callbacks
        self.platform = my_context.the_game.events_platform
        self.activate()

    def activate(self):
        if self.is_interrupt:
            self.platform.interrupts[self.target_event_cls.channel].add(self)
        else:
            self.platform.triggers[self.target_event_cls.channel].add(self)

    def check_conditions(self, event):
        assert isinstance(event, self.target_event_cls)
        for key, value in self.conditions.items():
            if getattr(event, key) != value:
                return False

        return True

    def try_on_event(self, event):
        if self.check_conditions(event):
            if self.effect_pack:
                self.effect_pack.resolve(self.source, event)
            if self.event_callbacks:
                for modifier in self.event_callbacks:
                    modifier(self, event)

    def deactivate(self):
        if self.is_interrupt:
            self.platform.interrupts[self.target_event_cls.channel].remove(self)
        else:
            self.platform.triggers[self.target_event_cls.channel].remove(self)


