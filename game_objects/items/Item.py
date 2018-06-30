class Item:
    def __init__(self, name, durability):
        assert isinstance(durability, int)
        assert isinstance(name, str)
        self.durability = durability
        self.name = name
        self.type = None