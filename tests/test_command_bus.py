from decimal import Decimal
from fx_platform.command_bus import CommandBus
from fx_platform.messages import PriceForwardCommand
from fx_platform.contracts import CurrencyPair, ForwardInput, ForwardResult

def test_command_bus_dispatch():
    bus = CommandBus()

    def handler(cmd: PriceForwardCommand):
        pair = cmd.input.pair
        forward = cmd.input.spot + Decimal("0.005")
        return ForwardResult(
            pair=pair,
            forward=forward,
            points=Decimal("0.005"),
            as_of=cmd.as_of
        )

    bus.register_handler(PriceForwardCommand, handler)

    pair = CurrencyPair(base="EUR", terms="USD")
    fi = ForwardInput(
        pair=pair,
        spot=Decimal("1.10"),
        domestic_rate=Decimal("0.02"),
        foreign_rate=Decimal("0.01"),
        tenor_in_years=Decimal("0.5"),
    )
    cmd = PriceForwardCommand(input=fi, as_of="2026-09-09")

    result = bus.dispatch(cmd)

    assert result.forward == Decimal("1.105")
    assert result.points == Decimal("0.005")
    assert result.pair.base == "EUR"
