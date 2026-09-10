# src/kernel/messages.py
from dataclasses import dataclass, field
from typing import Any, Optional, Dict
from datetime import datetime
import uuid
import copy

def make_trace_id() -> str:
    return str(uuid.uuid4())

def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


@dataclass(frozen=True)
class EventContext:
    """
    不可变的事件上下文，用于链路追踪与元数据传递。
    - trace_id: 全局链路 ID
    - timestamp: 事件时间 ISO 格式
    - source: 事件来源标识
    - request: 可选的原始请求负载
    - metadata: 可扩展的键值对
    """
    trace_id: str
    timestamp: str
    source: str
    request: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def with_metadata(self, extra: Dict[str, Any]) -> "EventContext":
        new_meta = dict(self.metadata or {})
        new_meta.update(extra)
        return EventContext(
            trace_id=self.trace_id,
            timestamp=self.timestamp,
            source=self.source,
            request=copy.deepcopy(self.request) if self.request is not None else None,
            metadata=new_meta
        )


@dataclass
class PriceForwardCommand:
    """
    命令对象，用于 forward 定价的输入校验。
    字段名使用 request 更语义化。
    """
    request: Dict[str, Any]

    def validate(self):
        missing = []
        for k in ("spot", "domestic_rate", "foreign_rate", "tenor"):
            if k not in self.request:
                missing.append(k)
        if missing:
            raise ValueError(f"PriceForwardCommand missing fields: {', '.join(missing)}")


@dataclass
class SpotPricedEvent:
    """
    事件：Spot 定价完成
    result 必须包含 'spot' 字段，且事件包含 as_of 时间戳
    """
    result: Dict[str, Any]
    context: EventContext
    event_bus: Optional[Any] = None

    def validate(self):
        if "spot" not in self.result:
            raise ValueError("SpotPricedEvent result missing 'spot'")
        if "as_of" not in self.result:
            raise ValueError("SpotPricedEvent result missing 'as_of'")


@dataclass
class ForwardPricedEvent:
    """
    事件：Forward 定价完成
    result 必须包含 'forward' 字段，且事件包含 as_of 时间戳
    """
    result: Dict[str, Any]
    context: EventContext
    event_bus: Optional[Any] = None

    def validate(self):
        if "forward" not in self.result:
            raise ValueError("ForwardPricedEvent result missing 'forward'")
        if "as_of" not in self.result:
            raise ValueError("ForwardPricedEvent result missing 'as_of'")


@dataclass
class AuditEvent:
    """
    审计事件，data 中必须包含 message 字段
    """
    data: Dict[str, Any]
    context: EventContext

    def validate(self):
        if "message" not in self.data:
            raise ValueError("AuditEvent data missing 'message'")


@dataclass
class MarketDataUpdatedEvent:
    """
    市场数据更新事件，data 必须包含 symbol 与 price
    """
    data: Dict[str, Any]
    context: EventContext
    event_bus: Optional[Any] = None

    def validate(self):
        if "symbol" not in self.data:
            raise ValueError("MarketDataUpdatedEvent 缺少 symbol")
        if "price" not in self.data:
            raise ValueError("MarketDataUpdatedEvent 缺少 price")


# 3️⃣ Query（查询）
@dataclass
class GetSpotQuery:
    """
    查询：获取现货价格，pair 为货币对字符串
    """
    pair: str

    def validate(self):
        if not isinstance(self.pair, str):
            raise ValueError("货币对必须是字符串")


