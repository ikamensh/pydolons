from my_utils.utils import clamp
from weakref import WeakKeyDictionary


class DynamicParameter:

    oldmax_names = set()

    @staticmethod
    def reset(unit):
        """
        Use this to give unit its max values
        """
        for oldmax_name in DynamicParameter.oldmax_names:
            try:
                delattr(unit, oldmax_name)
            except AttributeError:
                pass


    def __init__(self, max_name, on_zero_callbacks = None):
        cls = self.__class__
        prefix = cls.__name__
        self.max_name = max_name
        self.storage_name = f"{prefix}_{max_name}".replace("max", "")
        self.old_max_storage = f"{prefix}_{max_name}_oldmax".replace("max", "")
        DynamicParameter.oldmax_names.add(self.old_max_storage)

        self.on_zero_callbacks = on_zero_callbacks or []

    def __get__(self, unit, _):
        max_value = getattr(unit, self.max_name)
        if max_value is None:
            return None

        self._rescale(unit)
        return int(getattr(unit, self.storage_name))

    def __set__(self, unit, value):
        max_value = getattr(unit, self.max_name)
        if max_value is None:
            return
        new_value = clamp(value, 0, max_value)
        setattr(unit, self.storage_name, new_value)
        if new_value == 0:
            for callback in self.on_zero_callbacks:
                callback(unit)

    def _rescale(self, unit):
        new_max_value = getattr(unit, self.max_name)
        try:
            old_max_value = getattr(unit, self.old_max_storage)
        except AttributeError:
            setattr(unit, self.old_max_storage, new_max_value)
            setattr(unit, self.storage_name, new_max_value)
        else:
            if new_max_value == old_max_value:
                return
            percentage_full = getattr(unit, self.storage_name) / old_max_value
            setattr(unit, self.storage_name, int(new_max_value * percentage_full) )
            setattr(unit, self.old_max_storage, new_max_value)