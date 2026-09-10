from fx_platform.registry import ModuleRegistry, ModuleDescriptor

def test_module_registry_register_and_get():
    registry = ModuleRegistry()

    descriptor = ModuleDescriptor(
        name="pricing",
        capabilities=["forward.calculate"],
        health_check=lambda: True
    )

    registry.register(descriptor)
    retrieved = registry.get("pricing")

    assert retrieved.name == "pricing"
    assert retrieved.capabilities == ["forward.calculate"]
    assert retrieved.health_check() is True

def test_module_registry_list():
    registry = ModuleRegistry()

    registry.register(ModuleDescriptor(
        name="pricing",
        capabilities=["forward.calculate"],
        health_check=lambda: True
    ))

    registry.register(ModuleDescriptor(
        name="market_data",
        capabilities=["quote.read"],
        health_check=lambda: True
    ))

    modules = registry.list_modules()
    assert "pricing" in modules
    assert "market_data" in modules

def test_module_registry_health_check():
    registry = ModuleRegistry()

    registry.register(ModuleDescriptor(
        name="pricing",
        capabilities=["forward.calculate"],
        health_check=lambda: True
    ))

    registry.register(ModuleDescriptor(
        name="broken_module",
        capabilities=["none"],
        health_check=lambda: False
    ))

    results = registry.check_all()
    assert results["pricing"] is True
    assert results["broken_module"] is False
