class Active:
    def __init__(self, cost, events, user_targeting_type):
        self.cost = cost
        self.events = events
        self.user_targeting_type = user_targeting_type

    def assign_to_unit(self, owner):
        self.owner = owner

    def activate(self, user_targeting):
        """
        :param user_targeting: UserTargeting object containing the information given by the owner of the active
        :return: True if activation was successful, False otherwise
        """
        assert self.owner is not None
        if self.owner.can_pay(self.cost):
            self.owner.pay(self.cost)
            for event in self.events:
                event.resolve(self.owner, user_targeting)
            return True
        else:
            return False