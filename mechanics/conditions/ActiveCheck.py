from typing import List
from mechanics.conditions.ActiveCondition import ActiveCondition


class ActiveCheck:

    def __init__(self, conditions: List[ActiveCondition] = None):
        self.conditions = conditions or []

    def not_satisfied_conds(self, active, target) -> List[ActiveCondition]:
        result = [c for c in self.conditions if not c.evaluate(active, target)]
        return result
