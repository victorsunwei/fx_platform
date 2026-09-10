# tests/test_marketdata_spot.py
from kernel.event_bus import EventBus
from marketdata.provider import MarketDataProvider
from pricing.engine import PricingEngine
from pricing.handlers import on_audit

def test_marketdata_triggers_spot_and_audit(capfd):
    engine = PricingEngine(event_bus=EventBus())
    # engine._register_handlers 已注入 partial(on_marketdata_update, engine=self)
    engine.event_bus.subscribe("AuditEvent", on_audit)

    provider = MarketDataProvider(engine.event_bus)
    provider.publish_price("EURUSD", 1.2345, request={"source_test": True})

    captured = capfd.readouterr()
    assert "[MarketData]" in captured.out
    assert "[Audit]" in captured.out
