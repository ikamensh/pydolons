from mechanics.events import EventsChannels

class EventsPlatform:

    def __init__(self, gamelog):
        self.gamelog = gamelog
        self.interrupts = { ch: set() for ch in EventsChannels }
        self.triggers = { ch: set() for ch in EventsChannels }
        self.history = []

    def process_event(self, event):

        channel = event.channel
        interrupts = self.interrupts[channel]
        triggers = self.triggers[channel]

        for interrupt in list(interrupts):
            interrupt.try_on_event(event)

        if not event.interrupted and event.check_conditions():

            if self.history:
                for spy in self.history:
                    spy.append( (event, True) )

            if event.logging:
                self.gamelog(event)
            event.resolve()
            for trigger in list(triggers):
                trigger.try_on_event(event)

        else:
            if self.history:
                for spy in self.history:
                    spy.append( (event, False) )
            self.gamelog(f"{event}: INTERRUPTED")


    def collect_history(self):
        spy = []
        self.history.append(spy)
        return spy


