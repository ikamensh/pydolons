from mechanics.combat.AttackEvent import AttackEvent

def target_attacker(event):
    assert isinstance(event, AttackEvent)
    return event.source