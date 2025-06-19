from abc import ABC, abstractmethod
from typing import Optional
from models.user import User

class IUser(ABC):
    @abstractmethod
    def create(self, username: str, email: str, password: str, role: str = 'user') -> Optional[User]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
