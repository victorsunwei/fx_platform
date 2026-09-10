from decimal import Decimal
from fx_platform.event_bus import EventBus
from fx_platform.messages import ForwardPricedEvent
from fx_platform.contracts import CurrencyPair, ForwardResult

def test_event_bus_publish_and_subscribe():
    bus = EventBus()
    received = []

    def handler(evt: ForwardPricedEvent):
        received.append(evt.result.forward)

    bus.subscribe(ForwardPricedEvent, handler)

    pair = CurrencyPair(base="EUR", terms="USD")
    fr = ForwardResult(
        pair=pair,
        forward=Decimal("1.105"),
        points=Decimal("0.005"),
        as_of="2026-09-09"
    )
    evt = ForwardPricedEvent(result=fr, source="pricing_engine")

    bus.publish(evt)

    assert received == [Decimal("1.105")]
