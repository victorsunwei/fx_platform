# src/pricing/handlers.py
from kernel.messages import AuditEvent

def on_forward_priced(event):
    result = event.result
    ctx = event.context

    print(f"[Handler] Forward price computed: {result}")
    print(f"[Handler] trace_id: {ctx.trace_id} source: {ctx.source} timestamp: {ctx.timestamp}")
    if ctx.request is not None:
        print(f"[Handler] request: {ctx.request}")

    new_ctx = ctx.with_metadata({"stage": "audit", "handler": "on_forward_priced"})
    audit_evt = AuditEvent({"message": f"Forward price logged: {result}"}, context=new_ctx)
    audit_evt.validate()

    if getattr(event, "event_bus", None) is None:
        print("[Handler] warning: no event_bus available")
        return

    event.event_bus.publish(audit_evt)

def on_spot_priced(event):
    """
    Spot 定价完成后的 handler：记录并发布 AuditEvent（与 on_forward_priced 对称）
    """
    result = event.result
    ctx = event.context

    print(f"[Handler] Spot price computed: {result}")
    print(f"[Handler] trace_id: {ctx.trace_id} source: {ctx.source} timestamp: {ctx.timestamp}")
    if ctx.request is not None:
        print(f"[Handler] request: {ctx.request}")

    new_ctx = ctx.with_metadata({"stage": "audit", "handler": "on_spot_priced"})
    audit_evt = AuditEvent({"message": f"Spot price logged: {result}"}, context=new_ctx)
    audit_evt.validate()

    if getattr(event, "event_bus", None) is None:
        print("[Handler] warning: no event_bus available")
        return

    event.event_bus.publish(audit_evt)

def on_audit(event):
    ctx = event.context
    print(f"[Audit] {event.data['message']}")
    print(f"[Audit] trace_id: {ctx.trace_id} metadata: {ctx.metadata}")
    if ctx.request is not None:
        print(f"[Audit] request context: {ctx.request}")

def on_marketdata_update(event, engine=None):
    """
    解耦 handler：不直接做定价实现，而是通过注入的 engine 调用 engine.run。
    engine: PricingEngine 实例（由订阅时注入）
    """
    symbol = event.data["symbol"]
    price = event.data["price"]
    ctx = event.context

    print(f"[MarketData] {symbol} updated to {price} trace_id={ctx.trace_id}")

    if engine is None:
        # 兼容旧用法：如果没有注入 engine，仍然发布 AuditEvent 以保留现有行为
        audit_msg = f"MarketData update for {symbol} at {price}"
        audit_ctx = ctx.with_metadata({"stage": "marketdata", "symbol": symbol})
        audit_evt = AuditEvent({"message": audit_msg}, context=audit_ctx)
        audit_evt.validate()
        if getattr(event, "event_bus", None) is None:
            print("[MarketData] warning: no event_bus available")
            return
        event.event_bus.publish(audit_evt)
        return

    # 构造 spot 请求（根据 SpotPricing.price 接口调整）
    request = {"symbol": symbol, "spot": price, "tenor": 0}
    # 使用 engine.run 触发 spot 定价与后续事件（engine.run 会创建事件并 publish）
    engine.run("spot", request, source=ctx.source)


