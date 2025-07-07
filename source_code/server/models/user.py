from datetime import datetime
from typing import Optional

class User:
    def __init__(self, id: int, username: str, email: str, password_hash: str, role: str = 'user', created_at: Optional[datetime] = None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at or datetime.now()

    def is_admin(self) -> bool:
        return self.role == 'admin'

    def __repr__(self):
        return f"<User id={self.id}, username={self.username}, role={self.role}>"
