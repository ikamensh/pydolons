class Active:
    def __init__(self, targeting_cls, cost, callbacks):
        self.targeting_cls = targeting_cls
        self.cost = cost
        self.callbacks = callbacks
        self.owner = None

    def assign_to_unit(self, owner):
        self.owner = owner

    def activate(self, user_targeting):
        """
        :param user_targeting: UserTargeting object containing the information given by the owner of the active
        :return: True if activation was successful, False otherwise
        """
        assert isinstance(user_targeting, self.targeting_cls)
        assert self.owner is not None
        if self.owner.can_pay(self.cost):
            self.resolve(user_targeting)
            return True
        else:
            return False

    def resolve(self, targeting):
        self.owner.pay(self.cost)
        for callback in self.callbacks:
            callback(self, targeting)
