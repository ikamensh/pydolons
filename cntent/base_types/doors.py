from game_objects.battlefield_objects import Obstacle


def wooden_door(): return Obstacle("Wooden door", 250,
                                   armor=10, resists={}, icon="door.png")
