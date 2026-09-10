from pricing.spot import SpotPricing


def test_spot_price():
    engine = SpotPricing()
    assert engine.price({"spot": 100}) == 100
