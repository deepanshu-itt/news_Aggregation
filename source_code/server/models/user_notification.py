from typing import Optional, List, Dict


class UserNotification:
    def __init__(
        self,
        id: int,
        user_id: int,
        email_enabled: bool,
        daily_digest_enabled: bool,
        category_preferences: Optional[List[Dict[str, object]]] = None,
        email: Optional[str] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.email_enabled = email_enabled
        self.daily_digest_enabled = daily_digest_enabled
        self.category_preferences = category_preferences or []
        self.email = email

    def __repr__(self):
        return (
            f"<UserNotification user_id={self.user_id}, "
            f"email_enabled={self.email_enabled}, "
            f"daily_digest_enabled={self.daily_digest_enabled}, "
            f"category_preferences={self.category_preferences}>"
        )
