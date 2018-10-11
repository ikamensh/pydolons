from character_creation.Character import Character
from mechanics.AI.SimGame import SimGame as DreamGame
from cntent.base_types.demo_hero import demohero_basetype
from cntent.dungeons.demo_dungeon import demo_dungeon
from battlefield import Cell

from mechanics.events import Trigger
from multiplayer.events.ClientOrderRecievedEvent import ClientOrderRecievedEvent
from multiplayer.events.ClientOrderIssuedEvent import ClientOrderIssuedEvent

from multiplayer.socket_client import MyClient
from threading import Thread

import my_context


from GameLoopThread import GameLoopThread, ProxyEmit
from character_creation.Character import Character
from mechanics.AI.SimGame import SimGame as DreamGame
from cntent.base_types.demo_hero import demohero_basetype
from cntent.dungeons.demo_dungeon import demo_dungeon
from ui.TheUI import TheUI
from ui.triggers.animation_triggers import move_anim_trigger, damage_anim_trigger, attack_anin_trigger, \
    perish_anim_trigger, turn_anim_trigger, nexunit_anim_trigger, levelstatus_trigger, ui_error_message_trigger
from datetime import datetime

import sys

from PySide2 import QtWidgets


if __name__ == "__main__":

    client = MyClient()


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




    # Qt application initialization
    app = QtWidgets.QApplication(sys.argv)
    # The_hero character init
    character = Character(demohero_basetype)
    # Logical engine initialization, the_hero create from character
    print('cfg ===> start init DreamGame', datetime.now())
    # game = DreamGame.start_dungeon(walls_dungeon, character.unit)
    game = DreamGame.start_dungeon(demo_dungeon, character.unit, is_server=False)
    print('cfg ===> init DreamGame', datetime.now())
    # add character field for game
    game.character = character
    # Ui engine initialization
    window = TheUI(game)
    TheUI.singleton = window

    levelstatus_trigger(),
    ui_error_message_trigger(),
    nexunit_anim_trigger(),
    turn_anim_trigger(),
    perish_anim_trigger(),
    attack_anin_trigger(),
    damage_anim_trigger(),
    move_anim_trigger()

    order_issued_trigger()
    order_recieved_trigger()

    game.print_all_units()
    loop = GameLoopThread()


    # example correct stop thread
    def close_app():
        # game.loop stop condition
        game.loop_state = False
        # thread call quit, exit from thread
        loop.quit()
        # application waiting for shutdown thread
        loop.wait()


    # call exit from window
    app.aboutToQuit.connect(close_app)
    # set game and ui engine
    loop.game = game
    loop.the_ui = window
    # Qt signal initialization
    loop.setSiganls(ProxyEmit)
    # if the game_loop completes work then thread will completes its work
    # loop.start()
    client.connect()
    th = Thread(target=client.myreceive)
    th.start()
    sys.exit(app.exec_())

