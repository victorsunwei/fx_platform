from dataclasses import dataclass, field
from typing import Callable, Dict, List, Type


@dataclass
class EventBus:
    subscribers: Dict[Type, List[Callable]] = field(default_factory=dict)

    def subscribe(self, event_type: Type, handler: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def publish(self, event):
        event.validate()
        event_type = type(event)
        if event_type not in self.subscribers:
            return  # no subscribers
        for handler in self.subscribers[event_type]:
            handler(event)
