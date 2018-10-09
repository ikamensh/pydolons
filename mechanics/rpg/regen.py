from mechanics.events.src.Trigger import Trigger
from mechanics.events import TimePassedEvent
from cntent.abilities.undying import undead_n_hits
import my_context


FULL_REGEN_PERIOD = 3600
FULL_MANA_REGEN_PERIOD = 120
FULL_STAMINA_REGEN_PERIOD = 120


def regen_all_callback(t, e):
    for unit in my_context.the_game.battlefield.unit_locations.keys():
        if not unit.is_obstacle and unit.alive:
            is_undead = any([hasattr(a, undead_n_hits) for a in unit.abilities])
            if not is_undead:
                unit.health += unit.max_health * (2 * (unit.health / unit.max_health) - 1) * e.dt / FULL_REGEN_PERIOD

            unit.mana += unit.max_mana * e.dt / FULL_MANA_REGEN_PERIOD
            unit.stamina += unit.max_stamina * e.dt / FULL_STAMINA_REGEN_PERIOD


def regen_rule():
    return Trigger(TimePassedEvent,
                   conditions={},
                   callbacks=[regen_all_callback])