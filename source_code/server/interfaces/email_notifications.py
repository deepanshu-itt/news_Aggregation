from abc import ABC, abstractmethod
from typing import List, Optional
from models.email_notifications import EmailNotification


class IEmailNotificationRepository(ABC):

    @abstractmethod
    def create(self, notification: EmailNotification) -> Optional[EmailNotification]: pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> List[EmailNotification]: pass

    @abstractmethod
    def delete(self, notification_id: int) -> bool: pass
