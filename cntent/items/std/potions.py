from cntent.actives.callbacks_consumables import healing_potion_cb, mana_potion_cb, stamina_potion_cb
from game_objects.items import ChargedItem, ItemTypes
from mechanics.actives import ActiveTags

minor_healing_potion = ChargedItem("minor healing potion", use_callbacks=[healing_potion_cb(175)], tags=[ActiveTags.RESTORATION])
minor_mana_potion = ChargedItem("minor mana potion", use_callbacks=[mana_potion_cb(40)], tags=[ActiveTags.RESTORATION])
minor_stamina_potion = ChargedItem("minor stamina potion", use_callbacks=[stamina_potion_cb(12)], tags=[ActiveTags.RESTORATION])

rejuvination_potion = ChargedItem("rejuvination potion", max_charges=2,
                                  use_callbacks=[healing_potion_cb(135), mana_potion_cb(30), stamina_potion_cb(5)],
                                  tags=[ActiveTags.RESTORATION])


