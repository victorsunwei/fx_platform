# tests/test_marketdata.py
from kernel.event_bus import EventBus
from marketdata.provider import MarketDataProvider
from pricing.handlers import on_marketdata_update, on_audit

def test_marketdata_triggers_audit_and_handlers(capfd):
    bus = EventBus()
    # 订阅 MarketDataUpdatedEvent 到 marketdata handler
    bus.subscribe("MarketDataUpdatedEvent", on_marketdata_update)
    # 订阅 AuditEvent 到审计 handler，验证链路会触发审计
    bus.subscribe("AuditEvent", on_audit)

    provider = MarketDataProvider(bus)
    provider.publish_price("EURUSD", 1.2345, request={"source_test": True})

    captured = capfd.readouterr()
    assert "[MarketData]" in captured.out
    assert "[Audit]" in captured.out
