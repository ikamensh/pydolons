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
            interrupt.try_on_event(event)

        if not event.interrupted and event.check_conditions():
            if not isinstance(event, ActiveEvent) and not isinstance(event, NextUnitEvent):
                gamelog(event)
            event.resolve()
            for trigger in list(triggers):
                trigger.try_on_event(event)
        else:
            gamelog(repr(channel)+": INTERRUPTED")
