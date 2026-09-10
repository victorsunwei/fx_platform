# src/kernel/event_bus.py
import traceback

class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, handler):
        """
        event_type: 字符串，例如 "ForwardPricedEvent"
        handler: 可调用对象，接受单个参数 event
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def publish(self, event):
        """
        event: 事件实例，例如 ForwardPricedEvent(...)
        广播到所有订阅该事件类型的 handler。
        为避免单个 handler 抛错中断广播，捕获并记录异常。
        """
        event_type = event.__class__.__name__
        handlers = self.subscribers.get(event_type, [])

        for handler in handlers:
            try:
                handler(event)
            except Exception as exc:
                # 简单记录异常堆栈，避免中断其他 handler
                print(f"[EventBus] handler {handler.__name__ if hasattr(handler, '__name__') else handler} raised exception: {exc}")
                traceback.print_exc()
