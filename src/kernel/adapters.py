# src/kernel/adapters.py
class PricingAdapter:
    """
    把外部请求转换给 PricingEngine，并把 engine 的返回
    再转换成统一的响应格式。
    """

    def __init__(self, engine):
        self.engine = engine

    def run(self, request, product_type="forward"):
        """
        request: dict 原始请求（query）
        product_type: str, "spot" 或 "forward" 等
        返回统一格式的结果字典
        """
        # 直接调用 engine.run，让 engine 负责事件广播等逻辑
        value = self.engine.run(product_type, request)

        # 统一输出格式
        return {
            "type": "pricing_result",
            "value": value
        }
