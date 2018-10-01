from my_utils.named_enums import auto, NameEnum

class EventsChannels(NameEnum):
    DamageChannel = auto()
    HealingChannel = auto()

    MovementChannel = auto()
    TurnChannel = auto()
    AttackChannel = auto()

    ActiveChannel = auto()

    UnitDiedChannel = auto()
    ObstacleDestroyedChannel = auto()
    ItemDestroyedChannel = auto()

    BuffAppliedChannel = auto()
    BuffDetachedChannel = auto()
    BuffDispelledChannel = auto()
    BuffExpiredChannel = auto()

    NextUnitChannel = auto()

