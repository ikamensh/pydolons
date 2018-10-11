import time
from threading import Thread

import my_context
from battlefield import Cell
from character_creation.Character import Character
from cntent.base_types.demo_hero import demohero_basetype
from cntent.dungeons.demo_dungeon import demo_dungeon
from mechanics.AI.SimGame import SimGame as DreamGame
from mechanics.events import Trigger
from mechanics.fractions import Fractions
from multiplayer.events.ServerOrderIssuedEvent import ServerOrderIssuedEvent
from multiplayer.events.ServerOrderReceivedEvent import ServerOrderRecievedEvent
from multiplayer.network.ServerSocket import MyServer


def order_recieved_cb(t, e: ServerOrderRecievedEvent):
    g: DreamGame = my_context.the_game
    next_unit = g.turns_manager.get_next()
    fraction = g.fractions[next_unit]
    if e.fraction == fraction:
        unit = g.find_unit_by_uid(e.unit_uid)
        active = g.find_active_by_uid(e.active_uid)
        if isinstance(e.target, Cell):
            target = e.target
        else:
            target = g.find_unit_by_uid(e.target)

        g.order_action(unit, active, target)
    else:
        print(f"Order {e} was ignored. Active fraction is {fraction}")


def order_recieved_trigger():
    return Trigger(ServerOrderRecievedEvent,
                   conditions={},
                   callbacks=[order_recieved_cb])


def order_issued_cb(t, e):
    t.server.update_all(e)


def order_issued_trigger(server):
    t = Trigger(ServerOrderIssuedEvent,
                   conditions={},
                   callbacks=[order_issued_cb])
    t.server = server
    return t


class GameServer:

    def __init__(self):
        character  = Character(demohero_basetype)
        self.game = DreamGame.start_dungeon(demo_dungeon, character.unit)
        self.game.character = character
        self.server = MyServer(set(self.game.fractions.values()) - {Fractions.ENEMY, Fractions.NEUTRALS})

        order_issued_trigger(self.server)
        order_recieved_trigger()

    def listen(self):
        th = Thread(target=self.server.listen)
        th.start()

    def start_when_ready(self):
        while self.server.free_fractions:
            print(f"Waiting for {self.server.free_fractions}")
            time.sleep(1)

        print("The game has started.")
        self.game.loop()

if __name__ == "__main__":
    s = GameServer()
    s.listen()
    s.start_when_ready()