from character_creation.perks.PerkTree import PerkTree

from character_creation.perks.everymans_perks.group_attrib import pg_attributes
from character_creation.perks.everymans_perks.group_param import pg_params

import copy

def everymans_perks():
    return PerkTree([copy.deepcopy( pg_attributes ), copy.deepcopy( pg_params)] )


if __name__ == "__main__":
    from pprint import pprint

    ep = everymans_perks()
    
    pprint( ep.accessible_perks() )
    pprint( ep.cost_to_levelup( ep.accessible_perks()[0] ) )
    pprint( ep.cost_to_levelup( ep.accessible_perks()[1] ) )
    pprint( ep.cost_to_levelup( ep.accessible_perks()[2] ) )

    print('-*-'*50)


    str_perk = ep.accessible_perks()[0]
    agi_perk = ep.accessible_perks()[1]

    p1 = ep.accessible_perks()[3]
    p2 = ep.accessible_perks()[4]


    str_perk.current_level += 1

    pprint(ep.cost_to_levelup(ep.accessible_perks()[0]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[1]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[2]))
    print('-*-'*50)

    agi_perk.current_level += 1

    pprint(ep.cost_to_levelup(ep.accessible_perks()[0]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[1]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[2]))
    print('-*-'*50)

    str_perk.current_level += 1

    pprint(ep.cost_to_levelup(ep.accessible_perks()[0]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[1]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[2]))

    print('-*-'*50)
    p1.current_level += 1

    pprint(ep.cost_to_levelup(ep.accessible_perks()[0]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[1]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[2]))
    print('-*-'*50)

    p1.current_level += 1

    pprint(ep.cost_to_levelup(ep.accessible_perks()[0]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[1]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[2]))
    print('-*-'*50)

    p1.current_level += 1

    pprint(ep.cost_to_levelup(ep.accessible_perks()[0]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[1]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[2]))
    print('-*-'*50)

    p2.current_level += 1

    pprint(ep.cost_to_levelup(ep.accessible_perks()[0]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[1]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[2]))
    print('-*-'*50)

    p2.current_level += 1

    pprint(ep.cost_to_levelup(ep.accessible_perks()[0]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[1]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[2]))
    print('-*-'*50)

    p2.current_level += 1

    pprint(ep.cost_to_levelup(ep.accessible_perks()[0]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[1]))
    pprint(ep.cost_to_levelup(ep.accessible_perks()[2]))

