from dataclasses import dataclass
from datetime import date

@dataclass
class UserDto:
    username: str
    email: str
    password: str
    role: str= 'user'