from my_utils.named_enums import auto, NameEnum

class EventsChannels(NameEnum):
    DamageChannel = auto()
    HealingChannel = auto()

    MovementChannel = auto()
    PushChannel = auto()
    TurnChannel = auto()
    AttackChannel = auto()
    RangedAttackChannel = auto()

    ActiveChannel = auto()

    UnitDiedChannel = auto()
    ObstacleDestroyedChannel = auto()

    ItemDestroyedChannel = auto()
    UsedUpChannel = auto()
    DropChannel = auto()


    BuffAppliedChannel = auto()
    BuffDetachedChannel = auto()
    BuffDispelledChannel = auto()
    BuffExpiredChannel = auto()

    TimePassedChannel = auto()

    # UI
    NextUnitChannel = auto()
    LevelStatus = auto()
    UiErrorMessage = auto()

    # multiplayer
    ServerOrderIssuedChannel = auto()
    ServerOrderRecievedChannel = auto()
    ClientOrderIssuedChannel = auto()
    ClientOrderRecievedChannel = auto()

