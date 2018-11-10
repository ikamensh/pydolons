from typing import List
from mechanics.conditions.ActiveCondition import ActiveCondition


class ActiveCheck:

    def __init__(self, conditions: List[ActiveCondition] = None):
        self._conditions = conditions or []

    def not_satisfied_conds(self, active, target) -> List[ActiveCondition]:
        result = [c for c in self._conditions if not c.evaluate(active, target)]
        return result

    def append(self, cond: ActiveCondition):
        self._conditions.append(cond)
