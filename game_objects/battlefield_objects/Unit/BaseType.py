class BaseType:
    def __init__(self, str, agi, int, type_name, actives=set()):
        self.str = str
        self.agi = agi
        self.int = int
        self.type_name = type_name
        self.actives = actives