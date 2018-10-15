from game_objects.items import ItemTypes

class Item:
    def __init__(self, name, item_type, *, game=None):
        assert isinstance(name, str)
        assert isinstance(item_type, ItemTypes)
        self.item_type = item_type
        self.name = name
        self.game = game
        self.owner = None
        self.slot = None

    @property
    def tooltip_info(self):
        return {"name": f"{self.name}"}