from exceptions import PydolonsException

class InvalidTargetException(PydolonsException):

    def __init__(self, target, order):
        self.target = target
        self.order = order

    def __repr__(self):
        return f"Target {self.target} is invalid for the order {self.order}"