import inspect
import my_context

class Trigger:
    def __init__(self, target_event_cls, conditions = None,
                 source = None,
                 is_interrupt = False,
                 callbacks=None):

        assert inspect.isclass(target_event_cls)
        self.target_event_cls = target_event_cls
        self.conditions = conditions
        self.source = source
        self.is_interrupt = is_interrupt
        self.callbacks = callbacks
        self.platform = my_context.the_game.events_platform
        self.activate()

    def activate(self):
        if self.is_interrupt:
            self.platform.interrupts[self.target_event_cls.channel].add(self)
        else:
            self.platform.triggers[self.target_event_cls.channel].add(self)

    def check_conditions(self, event):
        assert isinstance(event, self.target_event_cls)
        if not self.conditions:
            return True
        return all((cond(self, event) for cond in self.conditions))

    def try_on_event(self, event):
        if self.check_conditions(event):
            if self.callbacks:
                for callback in self.callbacks:
                    callback(self, event)

    def deactivate(self):
        if self.is_interrupt:
            self.platform.interrupts[self.target_event_cls.channel].remove(self)
        else:
            self.platform.triggers[self.target_event_cls.channel].remove(self)


