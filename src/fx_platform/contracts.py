from dataclasses import dataclass
from decimal import Decimal

@dataclass
class CurrencyPair:
    base: str      # 例如 EUR
    terms: str     # 例如 USD

    def validate(self):
        assert len(self.base) == 3, "Base currency must be 3 letters"
        assert len(self.terms) == 3, "Terms currency must be 3 letters"
        assert self.base.isalpha(), "Base currency must be alphabetic"
        assert self.terms.isalpha(), "Terms currency must be alphabetic"
        assert self.base != self.terms, "Base and terms cannot be the same"

@dataclass
class MarketQuote:
    pair: CurrencyPair
    spot: Decimal

    def validate(self):
        self.pair.validate()
        assert self.spot > 0, "Spot must be positive"

@dataclass
class ForwardInput:
    pair: CurrencyPair
    spot: Decimal
    domestic_rate: Decimal
    foreign_rate: Decimal
    tenor_in_years: Decimal

    def validate(self):
        self.pair.validate()
        assert self.spot > 0, "Spot must be positive"
        assert self.tenor_in_years > 0, "Tenor must be positive"

@dataclass
class ForwardResult:
    pair: CurrencyPair
    forward: Decimal
    points: Decimal
    as_of: str     # 暂时用字符串，Day 5 再换成 datetime

    def validate(self):
        self.pair.validate()

