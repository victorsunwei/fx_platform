from pricing.engine import PricingEngine


def test_engine_forward():
    engine = PricingEngine()
    px = engine.run("forward", {
        "spot": 100,
        "domestic_rate": 0.05,
        "foreign_rate": 0.02,
        "tenor": 1
    })
    assert px > 0
