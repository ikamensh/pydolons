from game_objects.battlefield_objects import BattlefieldObject
from mechanics.damage import Resistances, Armor
from game_objects.attributes import DynamicParameter
from mechanics.events import ObstacleDestroyedEvent
from ui.sounds import sound_maps


class Obstacle(BattlefieldObject):

    sound_map = sound_maps.std_sound_map #TODO specific obstacle sound maps
    health = DynamicParameter("max_health", [lambda u : ObstacleDestroyedEvent(u)])

    is_obstacle = True

    def __init__(self, name, max_health, *, game=None, armor=0, resists=None, icon="wall.png"):
        super().__init__()
        self.game = game

        self.name = name
        self.max_health = max_health
        self.armor = armor if isinstance(armor,Armor) else Armor(base_value=armor)
        self.resists = resists or Resistances()
        self.melee_evasion = 0
        self.icon = icon
        self.alive = True
        self.last_damaged_by = None


    def lose_health(self, dmg_amount, source=None):

        assert dmg_amount >= 0
        if source:
            self.last_damaged_by = source
        self.health -= dmg_amount


    @property
    def tooltip_info(self):
        return {'name':f"{self.name}_{self.uid}",
                'hp':str(int(self.health)),
                'armor': repr(self.armor),
                'defence':str(self.melee_evasion)}

    def __repr__(self):
        return f"{self.name} alive {self.alive} with {self.health :.0f} HP"
