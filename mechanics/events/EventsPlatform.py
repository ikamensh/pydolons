# from utils.named_enums import auto, NameEnum
#
# class EventsChannels(NameEnum):
#     DamageDealtChannel = auto()
#     AttackStartedChannel = auto()
#     UnitDiedChannel = auto()
#     MovementCompleteChannel = auto()
from GameLog import gamelog

class EventsPlatform:

    triggers = set()

    @staticmethod
    def process_event(event):
        for trigger in EventsPlatform.triggers:
            if isinstance(event, trigger.target_event_cls):
                trigger.try_on_event(event)

        gamelog(event)
