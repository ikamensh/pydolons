from typing import List
from mechanics.conditions.ActiveCondition import ActiveCondition


class ActiveCheck:

    def __init__(self, conditions: List[ActiveCondition] = None):
        if conditions:
            try:
                iter(conditions)
            except TypeError:
                self._conditions = [conditions]
            else:
                self._conditions = conditions
        else:
            self._conditions = []

    def not_satisfied_conds(self, active, target) -> List[ActiveCondition]:
        result = [c for c in self._conditions if not c.evaluate(active, target)]
        return result

    def append(self, cond: ActiveCondition):
        self._conditions.append(cond)
