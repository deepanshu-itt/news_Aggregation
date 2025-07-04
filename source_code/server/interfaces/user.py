from abc import ABC, abstractmethod
from typing import Optional
from models.user import User
from dto.user_dto import UserDto


class IUser(ABC):
    @abstractmethod
    def create(self, user_data: UserDto) -> Optional[User]:
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
