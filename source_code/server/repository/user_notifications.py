import json
from database.database import db
from typing import Optional, List
from models.user_notification import UserNotification
from interfaces.user_notifications import IUserNotifications
from dto.cursor_dto import CursorDto
from repository.mysql_queries.user_notifications_queries import (
    create_user_notification_query,
    get_all_users_for_email,
    get_user_notification_by_id_query,
    update_user_notifications_query
)


class UserNotificationRepository(IUserNotifications):
    
    
    def find_by_user_id(self, user_id: int) -> Optional[UserNotification]:
        query = get_user_notification_by_id_query
        cursor_params = CursorDto(query=query, params=(user_id,), fetch_one=True)
        row = db.execute_query(cursor_params)

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
        category_preferences: List[int],
    ) -> UserNotification:
        existing = self.find_by_user_id(user_id)
        prefs_json = json.dumps(category_preferences or [])

        if existing:
            query = update_user_notifications_query
            cursor_params = CursorDto(query=query, params=(prefs_json, user_id), commit=True)
            db.execute_query(cursor_params)
            return UserNotification(existing.id, user_id, category_preferences, user_email)
        else:
            query = create_user_notification_query
            cursor_params = CursorDto(query=query, params=(user_id, prefs_json, user_email), commit=True)
            new_id = db.execute_query(cursor_params)
            return UserNotification(new_id, user_id, category_preferences, user_email)


    def get_users_for_daily_digest(self) -> List[UserNotification]:
        query = get_all_users_for_email

        cursor_params = CursorDto(query=query, fetch_all=True)
        rows = db.execute_query(cursor_params)
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
