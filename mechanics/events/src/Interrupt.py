from mechanics.events import Trigger

def interrupt_modifier(_, event):
    event.interrupted = True


class PermanentInterrupt(Trigger):
    def __init__(self, target_event_cls, conditions, interrupt_event = True, callbacks=None, *, platform):

        callbacks = callbacks or []
        if interrupt_event:
            callbacks.append(interrupt_modifier)


        super().__init__(target_event_cls, conditions=conditions, is_interrupt=True,
                         callbacks=callbacks, platform=platform)


class CounteredInterrupt(PermanentInterrupt):
    def __init__(self, target_event_cls, conditions, interrupt_event = True, callbacks:list=None,
                 n_counters=1, *, platform):

        self.n_counters = n_counters

        _callbacks = [CounteredInterrupt.count_down]
        if callbacks:
            _callbacks += callbacks



        super().__init__(target_event_cls, conditions, interrupt_event,
                         callbacks=_callbacks, platform=platform)

    @staticmethod
    def count_down(self, _):
        self.n_counters -= 1
        if self.n_counters <= 0:
            self.deactivate()