class Item:
    def __init__(self, durability):
        assert isinstance(durability, int)
        self.durability = durability
        self.type = None