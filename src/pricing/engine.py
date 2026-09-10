# src/pricing/engine.py
from typing import Optional
from functools import partial

from .spot import SpotPricing
from .forward import ForwardPricing
from .handlers import on_forward_priced, on_spot_priced, on_audit, on_marketdata_update
from kernel.event_bus import EventBus
from kernel.messages import (
    PriceForwardCommand,
    ForwardPricedEvent,
    SpotPricedEvent,
    EventContext,
    make_trace_id,
    now_iso,
)
from kernel.adapters import PricingAdapter


class PricingEngine:
    def __init__(self, event_bus: Optional[EventBus] = None):
        # 定价实现注册
        self.registry = {
            "spot": SpotPricing(),
            "forward": ForwardPricing(),
        }

        # 支持注入 event_bus（便于测试），否则创建默认实例
        self.event_bus = event_bus or EventBus()

        # 把订阅封装到单独方法，构造时调用
        self._register_handlers()

    def _register_handlers(self):
        # 订阅 forward 与 audit handler（保持原有行为）
        self.event_bus.subscribe("ForwardPricedEvent", on_forward_priced)
        self.event_bus.subscribe("SpotPricedEvent", on_spot_priced)
        self.event_bus.subscribe("AuditEvent", on_audit)
        # 注入 engine 给 marketdata handler（解耦 handler）
        self.event_bus.subscribe("MarketDataUpdatedEvent", partial(on_marketdata_update, engine=self))

    def run(self, product_type: str, request: dict, source: str = "pricing.adapter"):
        # 对 forward 使用命令校验；spot 请求通常字段不同所以不复用 PriceForwardCommand
        if product_type == "forward":
            cmd = PriceForwardCommand(request)
            cmd.validate()

        # 选择具体定价实现并计算
        engine_impl = self.registry[product_type]
        result = engine_impl.price(request)

        # 生成 trace id 与 timestamp，并构造不可变 context
        trace_id = make_trace_id()
        timestamp = now_iso()
        ctx = EventContext(trace_id=trace_id, timestamp=timestamp, source=source, request=request, metadata={})

        # 根据产品类型创建对应事件并发布
        if product_type == "forward":
            evt = ForwardPricedEvent({"forward": result, "as_of": timestamp}, context=ctx, event_bus=self.event_bus)
        else:  # spot
            evt = SpotPricedEvent({"spot": result, "as_of": timestamp}, context=ctx, event_bus=self.event_bus)

        evt.validate()
        self.event_bus.publish(evt)

        # 返回原始计算结果（adapter 会把它包装成统一格式）
        return result


# 模块级实例（导入 pricing 时不会触发订阅副作用）
engine = PricingEngine()
adapter = PricingAdapter(engine)

