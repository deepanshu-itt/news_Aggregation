from dataclasses import dataclass
from datetime import date

@dataclass
class APIRequest:
    base_url: str = None
    api_key: str = None
    query: str = None
    category: str = None
    from_date: date = None
    to_date: date = None