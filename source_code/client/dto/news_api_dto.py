from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class NewsApiDto:
    method: str
    endpoint: str
    data: Optional[Dict[str, Any]] = field(default=None)
    params: Optional[Dict[str, Any]] = field(default=None)
    current_user: Optional[Any] = field(default=None)
