import json
from database.database import db
from typing import Optional, List
from models.user_notification import UserNotification
from interfaces.user_notifications import IUserNotifications


class UserNotificationRepository(IUserNotifications):
    
    
    def find_by_user_id(self, user_id: int) -> Optional[UserNotification]:
        query = "SELECT * FROM user_notifications WHERE user_id = %s"
        row = db.execute_query(query, (user_id,), fetch_one=True)

        if row:
            row['category_preferences'] = self._parse_category_preferences(row.get('category_preferences'))
            return UserNotification(**row)
        return None


    def _parse_category_preferences(self, raw_json) -> list:
        if not raw_json:
            return []

        try:
            preferences = json.loads(raw_json)
            if isinstance(preferences, list):
                return [
                    {
                        "name": item.get("name"),
                        "keywords": item.get("keywords", []),
                        "enabled": item.get("enabled", True)
                    }
                    for item in preferences if isinstance(item, dict)
                ]
            return []
        except (json.JSONDecodeError, TypeError):
            return []


    def create_or_update(
        self,
        user_id: int,
        user_email: str,
        email_enabled: bool,
        daily_digest_enabled: bool,
        category_preferences: List[int],
    ) -> UserNotification:
        existing = self.find_by_user_id(user_id)
        prefs_json = json.dumps(category_preferences or [])

        if existing:
            query = """
                UPDATE user_notifications
                SET email_enabled = %s, daily_digest_enabled = %s, category_preferences = %s
                WHERE user_id = %s
            """
            db.execute_query(query, (email_enabled, daily_digest_enabled, prefs_json, user_id), commit=True)
            return UserNotification(existing.id, user_id, email_enabled, daily_digest_enabled, category_preferences, user_email)
        else:
            query = """
                INSERT INTO user_notifications (user_id, email_enabled, daily_digest_enabled, category_preferences)
                VALUES (%s, %s, %s, %s)
            """
            new_id = db.execute_query(query, (user_id, email_enabled, daily_digest_enabled, prefs_json), commit=True)
            return UserNotification(new_id, user_id, email_enabled, daily_digest_enabled, category_preferences, user_email)


    def get_users_for_daily_digest(self) -> List[UserNotification]:
        query = """
            SELECT un.*, u.email 
            FROM user_notifications un 
            JOIN users u ON un.user_id = u.id 
            WHERE daily_digest_enabled = TRUE AND email_enabled = TRUE
        """
        rows = db.execute_query(query, fetch_all=True)
        notifications = []
        for row in rows or []:
            row['category_preferences'] = self._parse_categories(row.get('category_preferences'))
            notifications.append(UserNotification(**row))
        return notifications


    def _parse_categories(self, raw) -> List[int]:
        if isinstance(raw, str):
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return []
        return raw or []
