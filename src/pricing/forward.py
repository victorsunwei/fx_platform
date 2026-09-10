from .contracts import PricingContract
from kernel.errors import PricingError
from kernel.logger import logger

forward_logger = logger.getChild("forward")

class ForwardPricing(PricingContract):
    def price(self, request):
        spot = request["spot"]
        r_dom = request["domestic_rate"]
        r_for = request["foreign_rate"]
        t = request["tenor"]

        price = spot * ((1 + r_dom) / (1 + r_for)) ** t

        if price < 0:
            forward_logger.error("价格不能为负数")
            raise PricingError("价格不能为负数")

        return price

