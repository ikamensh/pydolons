from content.active_packs.Fireball50 import fireball_pack
from mechanics.flexi_targeting.active.UserTargeting import CellTargeting
from battlefield.Battlefield import Cell

def test_fireball(game, hero, pirate_band):
    fireball_pack.resolve(hero, CellTargeting( Cell(4,4) ))

    for pirate in pirate_band:
        assert pirate.health < pirate.max_health


