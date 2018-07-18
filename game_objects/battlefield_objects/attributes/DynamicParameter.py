from utils.numeric import clamp
from weakref import WeakKeyDictionary
class DynamicParameter:

    initialized = WeakKeyDictionary()


    @staticmethod
    def reset(unit):
        """
        Use this to give unit its max values
        """
        if unit in DynamicParameter.initialized:
            del DynamicParameter.initialized[unit]


    def __init__(self, max_name, on_zero_callbacks = None):
        cls = self.__class__
        prefix = cls.__name__
        self.max_name = max_name
        self.storage_name = f"{prefix}_{max_name}".replace("max", "")
        self.max_values = WeakKeyDictionary()
        self.on_zero_callbacks = on_zero_callbacks or []

    def __get__(self, unit, _):
        max_value = getattr(unit, self.max_name)
        if max_value is None:
            return None
        if unit not in DynamicParameter.initialized:
            self._reset(unit)
            DynamicParameter.initialized[unit] = set()
            DynamicParameter.initialized[unit].add(self)
        elif self not in DynamicParameter.initialized[unit]:
            self._reset(unit)
            DynamicParameter.initialized[unit].add(self)
        else:
            self._rescale(unit)
        return getattr(unit, self.storage_name)

    def __set__(self, unit, value):
        max_value = getattr(unit, self.max_name)
        if max_value is None:
            return
        new_value = int(clamp(value, 0, max_value))
        if new_value == 0:
            for callback in self.on_zero_callbacks:
                callback(unit)
        setattr(unit, self.storage_name, new_value)

    def _reset(self, unit):
        max_value = getattr(unit, self.max_name)
        self.max_values[unit] = max_value
        setattr(unit, self.storage_name, max_value)

    def _rescale(self, unit):
        new_max_value = getattr(unit, self.max_name)
        if new_max_value == self.max_values[unit]:
            return
        percentage_full = getattr(unit, self.storage_name) / self.max_values[unit]
        setattr(unit, self.storage_name, int(new_max_value * percentage_full) )
        self.max_values[unit] = new_max_value