from dataclasses import dataclass, field
from typing import Callable, Dict, Type
from fx_platform.messages import PriceForwardCommand

@dataclass
class CommandBus:
    handlers: Dict[Type, Callable] = field(default_factory=dict)

    def register_handler(self, command_type: Type, handler: Callable):
        assert command_type not in self.handlers, f"Handler for {command_type} already registered"
        self.handlers[command_type] = handler

    def dispatch(self, command):
        command.validate()
        command_type = type(command)
        assert command_type in self.handlers, f"No handler registered for {command_type}"
        return self.handlers[command_type](command)
