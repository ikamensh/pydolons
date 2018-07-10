from mechanics.events.EventsPlatform import EventsPlatform


class Event:
    def __init__(self):
        EventsPlatform.process_event(self)

class DamageDealtEvent(Event):
    def __init__(self, source, target, amount, type):
        self.source = source
        self.target = target
        self.amount = amount
        self.type = type
        super().__init__()

    def __repr__(self):
        if self.amount == 0:
            "{} laughs at the attempts to damage it with {}".format(self.target, self.type)
        if self.source:
            return "{} recieves {} {} damage from {}.".format(self.target, self.amount, self.type, self.source)
        else:
            return "{} recieves {} {} damage.".format(self.target, self.amount, self.type)

class MovementCompletedEvent(Event):
    def __init__(self, unit, cell_from, cell_to):
        self.unit = unit
        self.cell_from = cell_from
        self.cell_to = cell_to
        super().__init__()

    def __repr__(self):
        return "{} moves from {} to {}".format(self.unit, self.cell_from, self.cell_to)

class UnitDiedEvent(Event):
    def __init__(self, unit, killer):
        self.unit = unit
        self.killer = killer
        super().__init__()

    def __repr__(self):
        if self.killer:
            if self.killer != self.unit:
                return "{} is killed by {}".format(self.unit, self.killer)
            else:
                return "{} commits suicide.".format(self.unit)
        else:
            return "{} dies.".format(self.unit)


class AttackStartedEvent(Event):
    def __init__(self, source, target):
        self.source = source
        self.target = target
        super().__init__()

    def __repr__(self):
        return "{} attacks {}.".format(self.source, self.target)

