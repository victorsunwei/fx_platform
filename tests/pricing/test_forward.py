from pricing.forward import ForwardPricing


def test_forward_price():
    engine = ForwardPricing()
    px = engine.price({
        "spot": 100,
        "domestic_rate": 0.05,
        "foreign_rate": 0.02,
        "tenor": 1
    })
    assert round(px, 2) == 102.94
