from dataclasses import dataclass, field
from typing import Dict, List, Callable

@dataclass
class ModuleDescriptor:
    name: str
    capabilities: List[str]
    health_check: Callable[[], bool]

    def validate(self):
        assert isinstance(self.name, str), "Module name must be a string"
        assert isinstance(self.capabilities, list), "Capabilities must be a list"
        assert callable(self.health_check), "Health check must be callable"

@dataclass
class ModuleRegistry:
    modules: Dict[str, ModuleDescriptor] = field(default_factory=dict)

    def register(self, descriptor: ModuleDescriptor):
        descriptor.validate()
        assert descriptor.name not in self.modules, f"Module {descriptor.name} already registered"
        self.modules[descriptor.name] = descriptor

    def get(self, name: str) -> ModuleDescriptor:
        assert name in self.modules, f"Module {name} not found"
        return self.modules[name]

    def list_modules(self) -> List[str]:
        return list(self.modules.keys())

    def check_all(self) -> Dict[str, bool]:
        return {name: desc.health_check() for name, desc in self.modules.items()}
