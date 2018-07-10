from mechanics.events.Event import AttackStartedEvent

def target_attacker(event):
    assert isinstance(event,AttackStartedEvent)
    return event.source