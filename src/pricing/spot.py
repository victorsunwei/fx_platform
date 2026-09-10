from .contracts import PricingContract
from kernel.errors import PricingError
from kernel.logger import logger

# 你要在这里加：模块自己的日志名字
spot_logger = logger.getChild("spot")

class SpotPricing(PricingContract):
    def price(self, request):
        price = request["spot"]

        # 你要在这里加：错误检查 + 写日志
        if price < 0:
            spot_logger.error("价格不能为负数")
            raise PricingError("价格不能为负数")

        return price
