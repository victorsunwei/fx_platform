from decimal import Decimal
from fx_platform.contracts import CurrencyPair, MarketQuote, ForwardInput, ForwardResult

def test_currency_pair_valid():
    pair = CurrencyPair(base="EUR", terms="USD")
    pair.validate()

def test_market_quote_valid():
    pair = CurrencyPair(base="EUR", terms="USD")
    quote = MarketQuote(pair=pair, spot=Decimal("1.10"))
    quote.validate()

def test_forward_input_valid():
    pair = CurrencyPair(base="EUR", terms="USD")
    fi = ForwardInput(
        pair=pair,
        spot=Decimal("1.10"),
        domestic_rate=Decimal("0.02"),
        foreign_rate=Decimal("0.01"),
        tenor_in_years=Decimal("0.5"),
    )
    fi.validate()

def test_forward_result_valid():
    pair = CurrencyPair(base="EUR", terms="USD")
    fr = ForwardResult(
        pair=pair,
        forward=Decimal("1.105"),
        points=Decimal("0.005"),
        as_of="2026-09-09"
    )
    fr.validate()
