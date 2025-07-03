from abc import ABC, abstractmethod
from typing import Optional, List
from models.user_notification import UserNotification

class IUserNotifications(ABC):
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[UserNotification]:
        pass


    @abstractmethod
    def create_or_update(
        self,
        user_id: int,
        user_email: str,
        category_preferences: List[int],
    ) -> UserNotification:
        pass


    @abstractmethod
    def get_users_for_daily_digest(self) -> List[UserNotification]:
        pass
