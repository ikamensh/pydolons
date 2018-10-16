from mechanics.events import ActiveEvent, EventsChannels, NextUnitEvent

class EventsPlatform:

    def __init__(self, gamelog):
        self.gamelog = gamelog
        self.interrupts = { ch: set() for ch in EventsChannels }
        self.triggers = { ch: set() for ch in EventsChannels }
        self.history = None

    def process_event(self, event):

        channel = event.channel
        interrupts = self.interrupts[channel]
        triggers = self.triggers[channel]

        for interrupt in list(interrupts):
            interrupt.try_on_event(event)

        if not event.interrupted and event.check_conditions():

            if self.history is not None:
                self.history.append( (event, True) )

            if not isinstance(event, ActiveEvent) and not isinstance(event, NextUnitEvent):
                self.gamelog(event)
            event.resolve()
            for trigger in list(triggers):
                trigger.try_on_event(event)

        else:
            if self.history is not None:
                self.history.append( (event, False) )
            self.gamelog(repr(channel)+": INTERRUPTED")

    def collect_history(self):
        self.history = []

    def stop_collect(self):
        self.history = None
