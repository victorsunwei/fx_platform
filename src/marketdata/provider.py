# src/marketdata/provider.py
from kernel.event_bus import EventBus
from kernel.messages import MarketDataUpdatedEvent, EventContext, make_trace_id, now_iso

class MarketDataProvider:
    def __init__(self, event_bus: EventBus, source: str = "marketdata.provider"):
        self.event_bus = event_bus
        self.source = source

    def publish_price(self, symbol: str, price: float, request: dict = None):
        trace_id = make_trace_id()
        timestamp = now_iso()
        ctx = EventContext(trace_id=trace_id, timestamp=timestamp, source=self.source, request=request or {}, metadata={})
        evt = MarketDataUpdatedEvent({"symbol": symbol, "price": price}, context=ctx, event_bus=self.event_bus)
        evt.validate()
        self.event_bus.publish(evt)
