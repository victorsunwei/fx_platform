from dataclasses import dataclass, field
from typing import List, Dict, Any
import datetime

@dataclass
class AuditRecord:
    timestamp: str
    actor: str
    action: str
    payload: Dict[str, Any]

    def validate(self):
        assert isinstance(self.timestamp, str)
        assert isinstance(self.actor, str)
        assert isinstance(self.action, str)
        assert isinstance(self.payload, dict)


@dataclass
class AuditTrail:
    records: List[AuditRecord] = field(default_factory=list)

    def log(self, actor: str, action: str, payload: Dict[str, Any]):
        record = AuditRecord(
            timestamp=datetime.datetime.utcnow().isoformat(),
            actor=actor,
            action=action,
            payload=payload
        )
        record.validate()
        self.records.append(record)

    def list_records(self) -> List[AuditRecord]:
        return self.records
