from character_creation.Character import Character
from mechanics.AI.SimGame import SimGame as DreamGame
from cntent.base_types.demo_hero import demohero_basetype
from cntent.dungeons.demo_dungeon import demo_dungeon
from battlefield import Cell

from mechanics.events import Trigger
from multiplayer.events.ClientOrderRecievedEvent import ClientOrderRecievedEvent
from multiplayer.events.ClientOrderIssuedEvent import ClientOrderIssuedEvent

from multiplayer.string_client import MyClient

import my_context


def one_game():
    character = Character(demohero_basetype)
    game = DreamGame.start_dungeon(demo_dungeon, character.unit)
    game.character = character
    game.print_all_units()
    game.loop()


if __name__ == "__main__":

    client = MyClient()


    def order_recieved_cb(t, e: ClientOrderRecievedEvent):

        g: DreamGame = my_context.the_game
        unit = g.find_unit_by_uid(e.unit_uid)
        active = g.find_active_by_uid(e.active_uid)
        if isinstance(e.target, Cell):
            target = e.target
        else:
            target = g.find_unit_by_uid(e.target)

        assert g.turns_manager.get_next() is unit

        unit.activate(active, target)
        g.player_turn_lock = False


    def order_recieved_trigger():
        return Trigger(ClientOrderRecievedEvent,
                       conditions={},
                       callbacks=[order_recieved_cb])


    def order_issued_cb(t, e):
        client.send(e)

    def order_issued_trigger():
        return Trigger(ClientOrderIssuedEvent,
                       conditions={},
                       callbacks=[order_issued_cb])


    order_issued_trigger()
    order_recieved_trigger()
    one_game()

