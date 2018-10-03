from GameLog import gamelog
from mechanics.events import ActiveEvent, EventsChannels, NextUnitEvent

class EventsPlatform:

    def __init__(self):
        self.interrupts = { ch: set() for ch in EventsChannels }
        self.triggers = { ch: set() for ch in EventsChannels }

    def process_event(self, event):
        channel = event.channel
        interrupts = self.interrupts[channel]
        triggers = self.triggers[channel]

        for interrupt in list(interrupts):
            assert isinstance(event, interrupt.target_event_cls)
            interrupt.try_on_event(event)

        if not event.interrupted and event.check_conditions():
            if not isinstance(event, ActiveEvent) and not isinstance(event, NextUnitEvent):
                gamelog(event)
            event.resolve()
            for trigger in list(triggers):
                if not isinstance(event, trigger.target_event_cls):
                    print(channel, trigger, event)
                trigger.try_on_event(event)
        else:
            gamelog(repr(channel)+": INTERRUPTED")
