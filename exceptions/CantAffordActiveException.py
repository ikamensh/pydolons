from exceptions import PydolonsException

class CantAffordActiveException(PydolonsException):

    def __init__(self, active, missing):
        assert missing in ["mana", "stamina", "health"]
        self.active = active
        self.missing = missing

    def __repr__(self):
        return f"Need more {self.missing} to activate {self.active}"