class Active:
    def __init__(self, cost, effect_pack):
        self.cost = cost
        self.effect_pack = effect_pack
        self.owner = None

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
            self.effect_pack.resolve(self.owner, user_targeting)
            return True
        else:
            return False