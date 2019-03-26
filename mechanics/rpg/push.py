from mechanics.events.src.Trigger import Trigger
from mechanics.events import MovementEvent, PushEvent

def push_callback(t, e: MovementEvent):
    bf = e.game.bf
    pusher = e.unit
    ctr = 0
    while bf.space_free( e.cell_to ) < 0 and len(bf.cells_to_objs[e.cell_to]) > 1 and \
            pusher.alive and ctr < 10:
        ctr += 1
        push_against = e.game.random.choice(list(set(bf.cells_to_objs[e.cell_to]) - {pusher}))
        PushEvent(pusher, push_against)


def push_condition(t, e):
    return e.game.bf.space_free( e.cell_to ) < 0

def push_rule(game):
    return Trigger(MovementEvent,
                   platform=game.events_platform,
                   conditions={push_condition},
                   callbacks=[push_callback])