from exceptions import PydolonsError

class InvalidTargetError(PydolonsError):

    def __init__(self, target, order):
        self.target = target
        self.order = order

    def __repr__(self):
        return f"Target.py {self.target} is invalid for the order {self.order}"