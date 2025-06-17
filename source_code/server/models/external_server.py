from datetime import datetime

class ExternalServer:
    def __init__(self, id, name, api_key, base_url, status='active',
                 last_accessed=None, created_at=None):
        self.id = id
        self.name = name
        self.api_key = api_key
        self.base_url = base_url
        self.status = status
        self.last_accessed = last_accessed or datetime.now()
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"<ExternalServer {self.name} (ID: {self.id})>"
