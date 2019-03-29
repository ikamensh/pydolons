# import pytest
# from multiplayer.Server import PydolonsServer
# from multiplayer.Client import PydolonsClient
#
# from threading import Thread
#
#
#
# @pytest.fixture()
# def client():
#     return PydolonsClient()
#
# def test_starts_same_state(client):
#     with PydolonsServer() as server:
#
#         client.start_sync()
#
#         sg = server.game
#         cg = client.game
#
#         for unit in sg.bf.unit_locations:
#             print(unit.uid)
#             mirror_double = cg.find_unit_by_uid(unit.uid + len(sg.bf.unit_locations))
#             assert mirror_double is not None
#             assert unit.type_name == mirror_double.type_name
#             assert unit.readiness == mirror_double.readiness
#
#             assert unit.health == mirror_double.health
#             assert unit.mana == mirror_double.mana
#             assert unit.stamina == mirror_double.stamina
#
#             assert unit.tooltip_info['damage'] == mirror_double.tooltip_info['damage']
#             assert unit.tooltip_info['armor'] == mirror_double.tooltip_info['armor']
#
#
#
# def test_server_orders_propagate():
#     #TODO
#     pass
#
# @pytest.mark.skip()
# def test_client_orders_executed():
#     #TODO
#     pass
#
# @pytest.mark.skip()
# def test_invalid_orders_ignored():
#     #TODO
#     pass
#
# @pytest.mark.skip()
# def test_small_battle_same_results():
#     #TODO
#     pass
