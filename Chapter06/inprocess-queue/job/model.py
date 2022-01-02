from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict
from uuid import UUID

import ujson as json


@dataclass
class JobDetails:
    uid: UUID
    name: str
    complete: bool
    timestamp: datetime
    kwargs: Dict[str, Any]
    return_value: Any

    def __json__(self):
        output = asdict(self)
        output["uid"] = str(self.uid)
        output["timestamp"] = self.timestamp.isoformat()
        return json.dumps(output)
