from __future__ import annotations
import inspect
from typing import TYPE_CHECKING, ClassVar, List, Callable, Collection
if TYPE_CHECKING:
    from mechanics.events import EventsPlatform
    from game_objects.battlefield_objects import Unit

class Trigger:
    def __init__(self, target_event_cls: ClassVar,*, platform: EventsPlatform, conditions: Collection[Callable] = None,
                 source: Unit = None,
                 is_interrupt: bool = False,
                 callbacks: List[Callable] = None):

        assert inspect.isclass(target_event_cls)
        self.channel = target_event_cls.channel
        self.conditions = conditions
        self.source = source
        self.is_interrupt = is_interrupt
        self.callbacks = callbacks
        self.platform = platform
        self.activate()

    def activate(self):
        if self.is_interrupt:
            self.platform.interrupts[self.channel].add(self)
        else:
            self.platform.triggers[self.channel].add(self)

    def check_conditions(self, event):
        if not self.conditions:
            return True
        return all((cond(self, event) for cond in self.conditions))

    def try_on_event(self, event):
        if self.check_conditions(event):
            if self.callbacks:
                for callback in self.callbacks:
                    callback(self, event)
        # else: #easier debug!
        #     print([cond(self,event) for cond in self.conditions])

    def deactivate(self):
        try:
            if self.is_interrupt:
                self.platform.interrupts[self.channel].remove(self)
            else:
                self.platform.triggers[self.channel].remove(self)
        except KeyError:
            pass


