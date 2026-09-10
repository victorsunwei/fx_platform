from dataclasses import dataclass
from decimal import Decimal
from fx_platform.contracts import CurrencyPair, ForwardInput, ForwardResult

@dataclass
class PriceForwardCommand:
    input: ForwardInput
    as_of: str

    def validate(self):
        self.input.validate()
        assert isinstance(self.as_of, str), "as_of must be a string"

@dataclass
class ForwardPricedEvent:
    result: ForwardResult
    source: str

    def validate(self):
        self.result.validate()
        assert self.source in ["pricing_engine", "market_data"], "Invalid event source"

@dataclass
class GetMarketQuoteQuery:
    pair: CurrencyPair

    def validate(self):
        self.pair.validate()
