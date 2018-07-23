from mechanics.events import Trigger

def interrupt_modifier(_, event):
    event.interrupted = True


class PermanentInterrupt(Trigger):
    def __init__(self, target_event_cls, conditions, interrupt_event = True, event_callbacks=None):

        callbacks = []
        if interrupt_event:
            callbacks.append(interrupt_modifier)
        if event_callbacks:
            callbacks.extend(event_callbacks)

        super().__init__(target_event_cls, conditions, is_interrupt=True,
                         event_callbacks=callbacks)


class CounteredInterrupt(PermanentInterrupt):
    def __init__(self, target_event_cls, conditions, interrupt_event = True,event_callbacks=None,
                 n_counters=1):

        self.n_counters = n_counters

        callbacks = event_callbacks or []
        callbacks.append(CounteredInterrupt.count_down)


        super().__init__(target_event_cls, conditions, interrupt_event,
                         event_callbacks=callbacks)

    @staticmethod
    def count_down(self, _):
        self.n_counters -= 1
        if self.n_counters <= 0:
            self.deactivate()