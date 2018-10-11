from character_creation.Character import Character
from mechanics.AI.SimGame import SimGame as DreamGame
from cntent.base_types.demo_hero import demohero_basetype
from cntent.dungeons.demo_dungeon import demo_dungeon
from battlefield import Cell

from mechanics.events import Trigger
from multiplayer.events.ServerOrderReceivedEvent import ServerOrderRecievedEvent
from multiplayer.events.ServerOrderIssuedEvent import ServerOrderIssuedEvent
from multiplayer.socket_server import MyServer

import my_context

from threading import Thread
import time

from mechanics.fractions import Fractions

if __name__ == "__main__":

    character  = Character(demohero_basetype)
    game = DreamGame.start_dungeon(demo_dungeon, character.unit)
    game.character = character
    game.print_all_units()

    server = MyServer(set(game.fractions.values()) - {Fractions.ENEMY, Fractions.NEUTRALS})

    def order_recieved_cb(t, e:ServerOrderRecievedEvent):
        g:DreamGame = my_context.the_game
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
        server.update_all(e)

    def order_issued_trigger():
        return Trigger(ServerOrderIssuedEvent,
                       conditions={},
                       callbacks=[order_issued_cb])

    order_issued_trigger()
    order_recieved_trigger()

    th = Thread(target=server.listen)
    th.start()

    while server.free_fractions:
        print(f"Waiting for {server.free_fractions}")
        time.sleep(1)

    print("The game has started.")
    game.loop()

