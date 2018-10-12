import sys
from threading import Thread

from PySide2 import QtWidgets

import my_context
from GameLoopThread import GameLoopThread, ProxyEmit
from battlefield import Cell
from character_creation.Character import Character
from cntent.base_types.demo_hero import demohero_basetype
from cntent.dungeons.demo_dungeon import demo_dungeon
from mechanics.AI.SimGame import SimGame as DreamGame
from mechanics.events import NextUnitEvent
from mechanics.events import Trigger
from multiplayer.events.ClientOrderIssuedEvent import ClientOrderIssuedEvent
from multiplayer.events.ClientOrderRecievedEvent import ClientOrderRecievedEvent
from multiplayer.network.ClientSocket import ClientSocket
from ui.TheUI import TheUI
from ui.triggers.animation_triggers import move_anim_trigger, damage_anim_trigger, attack_anin_trigger, \
    perish_anim_trigger, turn_anim_trigger, nexunit_anim_trigger, levelstatus_trigger, ui_error_message_trigger


def order_recieved_cb(t, e: ClientOrderRecievedEvent):
    g: DreamGame = my_context.the_game
    unit = g.find_unit_by_uid(e.unit_uid)
    active = g.find_active_by_uid(e.active_uid)
    if e.target is None:
        target = None
    elif isinstance(e.target, Cell):
        target = e.target
    else:
        target = g.find_unit_by_uid(e.target)

    assert g.turns_manager.get_next() is unit

    unit.activate(active, target)
    NextUnitEvent(g.turns_manager.get_next())
    g.player_turn_lock = False


def order_recieved_trigger():
    return Trigger(ClientOrderRecievedEvent,
                   conditions={},
                   callbacks=[order_recieved_cb])

def order_issued_cb(t, e):
    t.client.send(e)

def order_issued_trigger(client):
    t = Trigger(ClientOrderIssuedEvent,
                   conditions={},
                   callbacks=[order_issued_cb])
    t.client = client
    return t



class GameClient:

    def __init__(self):
        self.client = ClientSocket()

        character = Character(demohero_basetype)
        self.game = DreamGame.start_dungeon(demo_dungeon, character.unit, is_server=False)
        self.game.character = character

        order_issued_trigger(self.client)   # local actions cause sending orders to the server
        order_recieved_trigger()            # orders from the server cause local actions

    def start_sync(self):
        self.client.connect()
        th = Thread(target=self.client.myreceive)
        th.start()



    def start_gui(self):

        app = QtWidgets.QApplication(sys.argv)

        window = TheUI(self.game)
        TheUI.singleton = window

        levelstatus_trigger(),
        ui_error_message_trigger(),
        nexunit_anim_trigger(),
        turn_anim_trigger(),
        perish_anim_trigger(),
        attack_anin_trigger(),
        damage_anim_trigger(),
        move_anim_trigger()

        loop = GameLoopThread()

        def close_app():
            self.game.loop_state = False
            loop.quit()
            # application waiting for shutdown thread
            loop.wait()


        # call exit from window
        app.aboutToQuit.connect(close_app)
        loop.game = self.game
        loop.the_ui = window
        # Qt signal initialization
        loop.setSiganls(ProxyEmit)
        sys.exit(app.exec_())

if __name__ == "__main__":
    c = GameClient()
    c.start_sync()
    c.start_gui()
