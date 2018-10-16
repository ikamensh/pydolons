from abc import ABC

class BattlefieldObject(ABC):

    last_uid = 0
    uid = None
    is_obstacle = None
    melee_evasion = 0
    alive = None
    game = None
    health = None



    def lose_health(self, amount, source = None):
        raise NotImplementedError