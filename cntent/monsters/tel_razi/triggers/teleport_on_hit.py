from __future__ import annotations
from mechanics.events import Trigger
from mechanics.events import AttackEvent, MovementEvent

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit


def random_teleport_callback(t: Trigger, e: AttackEvent):
    unit: Unit = e.target
    if not unit.alive:
        return

    cost = t.random_teleport_cost
    chance = t.random_teleport_chance
    radius = t.random_teleport_radius

    if unit.can_pay(cost):

        if e.game.random.random() < chance:
            initial_location = unit.cell
            possible_cells = e.game.bf.neighbours_exclude_center(
                initial_location, radius)
            target_cell = e.game.random.choice(possible_cells)
            MovementEvent(unit, target_cell)
            unit.pay(cost)


def random_teleport_trigger(unit, radius, chance, cost):
    trig = Trigger(AttackEvent,
                   platform=unit.game.events_platform,
                   conditions={lambda t, e: e.target.uid == unit.uid},
                   callbacks=[random_teleport_callback])

    trig.random_teleport_radius = radius
    trig.random_teleport_chance = chance
    trig.random_teleport_cost = cost

    return trig
