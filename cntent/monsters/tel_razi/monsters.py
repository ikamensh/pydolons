from mechanics.actives import Cost
from cntent.monsters.tel_razi.abilities.teleport_on_hit import teleport_on_hit
from cntent.monsters.tel_razi.actives import tel_razi_electrify
from cntent.monsters.tel_razi.actives import sentinel_shot
from cntent.monsters.tel_razi.abilities.zone_control import zone_control_damage
from cntent.abilities.generic.ability import fat
from cntent.monsters.tel_razi.abilities.golem_n_charges import golem_n_charges
from cntent.items.std import std_items, std_ranged

from game_objects.battlefield_objects import BaseType
from game_objects.monsters.Monster import Monster


class golems_sound_map:
    move = "SftStep3.wav"
    hit = "c_ghast_hit2.mp3"
    attack = "c_ghast_atk1.mp3"
    perish = "c_ghast_death.mp3"


golem_bt = BaseType({'str': 24,
                     'end': 15,
                     'prc': 0,
                     'agi': 2,
                     'int': 2,
                     'cha': 8},
                    "Crude Golem",
                    abilities=[golem_n_charges(15),
                               fat],
                    icon=["golem.png"],
                    sound_map=golems_sound_map)

golem = Monster(golem_bt,
                [

                ])


sentinel_bt = BaseType({'str': 9,
                        'end': 13,
                        'prc': 18,
                        'agi': 12,
                        'int': 12,
                        'cha': 8},
                       "Sentinel",
                       abilities=[golem_n_charges(12),
                                  zone_control_damage(3,
                                                      0.5)],
                       actives=[sentinel_shot],
                       icon=["sentinel.jpg"],
                       sound_map=golems_sound_map)

sentinel = Monster(sentinel_bt,
                   [

                   ])


class tel_razi_sound_map:
    move = "SftStep3.wav"
    hit = "c_ghast_hit2.mp3"
    attack = "c_ghast_atk1.mp3"
    perish = "c_ghast_death.mp3"


tel_razi_scrub_bt = BaseType({'str': 5,
                              'end': 8,
                              'prc': 16,
                              'agi': 12,
                              'int': 21,
                              'cha': 12},
                             actives=[tel_razi_electrify],
                             abilities=[teleport_on_hit(3,
                                                        0.8,
                                                        Cost(stamina=1,
                                                             mana=5,
                                                             readiness=0.1))],
                             type_name="Tel'Razi Scrub",
                             icon=["wormface.jpg"],
                             sound_map=tel_razi_sound_map)

tel_razi_scrub = Monster(tel_razi_scrub_bt, [[std_items.jacket_cheap], [
                         std_ranged.black_bow, std_ranged.cheap_bow, std_ranged.quality_crossbow]])

tel_razi_zealot_bt = BaseType({'str': 15,
                               'end': 16,
                               'prc': 16,
                               'agi': 21,
                               'int': 12,
                               'cha': 12},
                              actives=[tel_razi_electrify],
                              abilities=[teleport_on_hit(2,
                                                         0.5,
                                                         Cost(stamina=1,
                                                              mana=5,
                                                              readiness=0.1))],
                              type_name="Tel'Razi Zealot",
                              icon=["wormface2.jpg"],
                              sound_map=tel_razi_sound_map)

tel_razi_zealot = Monster(tel_razi_zealot_bt,
                          [[std_items.jacket_cheap,
                            std_items.jacket_trollhide],
                           [std_items.sword_superior,
                              std_items.axe_superior,
                              std_items.spear_superior]])
