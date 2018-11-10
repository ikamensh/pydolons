from game_objects.spells import  SpellConcept
from character.masteries.MasteriesEnumSimple import MasteriesEnum
from mechanics.actives import Cost
from cntent.spells.fire.burning_hands.callbacks import burning_hands_callback
from cntent.spells.fire.immolation.callbacks import immolation_callback
from game_objects.battlefield_objects import BattlefieldObject


burning_hands_concept = SpellConcept(name="burning hands",
                                 school=MasteriesEnum.FIRE,
                                 targeting_cls=None,
                                 complexity=15,
                                 cost=Cost(3, 25, 0, readiness=1),
                                 cooldown=4,
                                 amount=25, duration=None, precision_factor=1,
                                 distance=3, radius=2,
                                 resolve_callback=burning_hands_callback)


immolation_concept = SpellConcept(name="immolation",
                                 school=MasteriesEnum.FIRE,
                                 targeting_cls=BattlefieldObject,
                                 complexity=8,
                                 cost=Cost(3, 25, 0, readiness=1),
                                 cooldown=4,
                                 amount=25, duration=4, precision_factor=1,
                                 distance=3, radius=None,
                                 resolve_callback=immolation_callback)
