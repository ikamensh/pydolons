from typing import Callable, TYPE_CHECKING


class TriggerCondition:
    def __init__(self, name: str, expr: Callable, message_fmt: str):
        self.expr = expr
        self.message_fmt = message_fmt
        self.name = name

    def evaluate(self, event, trigger):
        return self.expr(event, trigger)

    def message(self, event, trigger):
        return self.message_fmt.format(event, trigger, self.name)