from mechanics.events.src.Trigger import Trigger
from mechanics.events import MovementEvent, DamageEvent

from mechanics.factions import Faction



# no bleeding?
def gain_aggro_cb(t, e: MovementEvent):

    passive_enemies = [u for u in e.game.units
                       if e.game.factions[u] is Faction.ENEMY and not u.fights_hero]

    player_units = [u for u in e.game.units if e.game.factions[u] is Faction.PLAYER]

    for enemy in passive_enemies:
        for ally in player_units:
            if e.battlefield.x_sees_y(enemy, ally):
                enemy.fights_hero = True
                break


def lose_agro_cb(t, e: MovementEvent):
    active_enemies = [u for u in e.game.units
                       if e.game.factions[u] is Faction.ENEMY and u.fights_hero]

    player_units = [u for u in e.game.units if e.game.factions[u] is Faction.PLAYER]

    def min_distance(enemy):
        return min([e.battlefield.distance(enemy, ally) for ally in player_units])

    for enemy in active_enemies:
        if min_distance(enemy) > enemy.sight_range * 2:
            enemy.fights_hero = False




def vision_aggro_rule(game):
    return Trigger(MovementEvent,
                   platform=game.events_platform,
                   conditions={},
                   callbacks=[gain_aggro_cb, lose_agro_cb])


# no bleeding?
def damage_provokes_cb(t, e: DamageEvent):

    damage_from_player = e.game.factions[e.source] is Faction.PLAYER
    if damage_from_player:
        e.target.fights_hero = True


def damage_provokes_rule(game):
    return Trigger(DamageEvent,
                   platform=game.events_platform,
                   conditions={},
                   callbacks=[damage_provokes_cb])