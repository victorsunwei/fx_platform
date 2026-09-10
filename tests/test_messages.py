from decimal import Decimal
from fx_platform.contracts import CurrencyPair, ForwardInput, ForwardResult
from fx_platform.messages import PriceForwardCommand, ForwardPricedEvent, GetMarketQuoteQuery

def test_price_forward_command_valid():
    pair = CurrencyPair(base="EUR", terms="USD")
    fi = ForwardInput(
        pair=pair,
        spot=Decimal("1.10"),
        domestic_rate=Decimal("0.02"),
        foreign_rate=Decimal("0.01"),
        tenor_in_years=Decimal("0.5"),
    )
    cmd = PriceForwardCommand(input=fi, as_of="2026-09-09")
    cmd.validate()

def test_forward_priced_event_valid():
    pair = CurrencyPair(base="EUR", terms="USD")
    fr = ForwardResult(pair=pair, forward=Decimal("1.105"), points=Decimal("0.005"), as_of="2026-09-09")
    evt = ForwardPricedEvent(result=fr, source="pricing_engine")
    evt.validate()

def test_get_market_quote_query_valid():
    pair = CurrencyPair(base="EUR", terms="USD")
    q = GetMarketQuoteQuery(pair=pair)
    q.validate()
