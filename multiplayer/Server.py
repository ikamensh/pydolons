import time
from threading import Thread

from battlefield import Cell
from character.Character import Character
from cntent.base_types.demo_hero import demohero_basetype
from cntent.dungeons.demo_dungeon import demo_dungeon
from mechanics.AI.SimGame import SimGame as DreamGame
from mechanics.events import Trigger
from mechanics.factions import Faction
from multiplayer.events.ServerOrderIssuedEvent import ServerOrderIssuedEvent
from multiplayer.events.ServerOrderReceivedEvent import ServerOrderRecievedEvent
from multiplayer.network.ServerSocket import ServerSocket


def order_recieved_cb(t, e: ServerOrderRecievedEvent):
    g: DreamGame = e.game
    next_unit = g.turns_manager.get_next()
    fraction = g.factions[next_unit]
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


def order_recieved_trigger(game):
    return Trigger(ServerOrderRecievedEvent,
                   platform=game.events_platform,
                   conditions={},
                   callbacks=[order_recieved_cb])


def order_issued_cb(t, e):
    t.server.update_all(e)


def order_issued_trigger(game, server):
    t = Trigger(ServerOrderIssuedEvent,
                platform=game.events_platform,
                conditions={},
                   callbacks=[order_issued_cb])
    t.server = server
    return t


class PydolonsServer:

    def __init__(self):
        character  = Character(demohero_basetype)
        self.game = DreamGame.start_dungeon(demo_dungeon, character.unit)
        self.game.character = character
        self.server_socket = ServerSocket(self.game, set(self.game.fractions.values()) - {Faction.ENEMY,
                                                                                          Faction.NEUTRALS})

        order_issued_trigger(self.game, self.server_socket)
        order_recieved_trigger(self.game)

    def listen(self):
        th = Thread(target=self.server_socket.listen)
        th.start()

    def start_when_ready(self):
        def wait_into_game_loop():
            while self.server_socket.free_fractions:
                print(f"Waiting for {self.server_socket.free_fractions}")
                time.sleep(1)

            print("The game has started.")
            self.game.loop()

        th = Thread(target=wait_into_game_loop)
        th.start()

    def __enter__(self):
        self.listen()
        self.start_when_ready()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server_socket.serversocket.close()

if __name__ == "__main__":
    s = PydolonsServer()
    s.listen()
    s.start_when_ready()