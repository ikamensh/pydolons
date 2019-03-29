from typing import Callable


class ActiveCondition:
    def __init__(self, name: str, expr: Callable, message_fmt: str):
        self.expr = expr
        self.message_fmt = message_fmt
        self.name = name

    def evaluate(self, active, target):
        return self.expr(active, target)

    def message(self, active, target):
        return self.message_fmt.format_map(
            {"active": active, "target": target, "cond_name": self.name})

    def __repr__(self):
        return f"{self.name} active condition"
