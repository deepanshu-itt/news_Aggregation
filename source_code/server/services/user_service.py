from repository.user_notifications import UserNotificationRepository
from repository.email_notification_repository import EmailNotificationRepository
from repository.user_repository import UserRepository
from models.user import User
from repository.news_article_repository import NewsArticleRepository
from utils.preferences_utils import (
    merge_keywords_into_preferences,
    remove_keywords_from_category,
    remove_category_from_preferences,
)

user_notification_manager = UserNotificationRepository()


class UserService:

    @staticmethod
    def get_user_profile(user_id):
        user_manager = UserRepository()
        user = user_manager.find_by_user_id(user_id)
        if user:
            prefs = user_notification_manager.find_by_user_id(user_id)
            prefs_data = {
                'category_preferences': prefs.category_preferences if prefs else []
            }
            return {"success": True, "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "preferences": prefs_data
            }}, 200

        return {"success": False, "message": "User not found."}, 404


    @staticmethod
    def get_user_email_notifications(user_id):
        email_notification_manager = EmailNotificationRepository()
        user_email_notifications = email_notification_manager.get_by_user(user_id)
        if user_email_notifications:
            data = [
                {
                    "id": email_notification.id,
                    "user_id": email_notification.user_id,
                    "article_ids": email_notification.article_ids,
                    "message": email_notification.message,
                    "sent_at": email_notification.sent_at
                }
                for email_notification in user_email_notifications
            ]
            return {"success": True, "notifications": data}, 200

        return {"success": True, "message": "No notifications found"}, 404


    @staticmethod
    def update_user_preferences(user_id, category_name: str, category_preferences):
        user_manager = UserRepository()
        already_data = user_notification_manager.find_by_user_id(user_id)
        user = user_manager.find_by_user_id(user_id)
        if not user:
            return {"success": False, "message": "User not found."}, 404

        if not already_data:
            notification_prefs = UserService.create_preferences(user, category_name, category_preferences)
        else:
            notification_prefs = UserService.update_keywords(user, category_name, category_preferences)

        if notification_prefs:
            return {"success": True, "message": "Preferences updated successfully."}, 200

        return {"success": False, "message": "Failed to update preferences."}, 500


    @staticmethod
    def create_preferences(user: User, category_name: str, category_preferences):
        updated_preferences = [
            {
                "name": category_name,
                "enabled": True,
                "keywords": category_preferences
            }
        ]

        return user_notification_manager.create_or_update(
            user.id, user.email, updated_preferences
        )


    @staticmethod
    def update_keywords(user: User, category_name: str, category_preferences):
        category_preferences = list(set(category_preferences))
        existing_data = user_notification_manager.find_by_user_id(user.id)

        updated_preferences = merge_keywords_into_preferences(
            existing_data.category_preferences,
            category_name,
            category_preferences
        )

        return user_notification_manager.create_or_update(
            user.id, user.email, updated_preferences
        )


    @staticmethod
    def remove_notification_keyword(user_id: int, category_name: str, keyword):
        user_manager = UserRepository()
        user = user_manager.find_by_user_id(user_id)
        if not user:
            return {"success": False, "message": "User not found"}, 404

        return UserService.handle_preferences_updation(user.id, category_name, keyword)


    @staticmethod
    def handle_preferences_updation(userid, category_name, keyword=None):
        if not keyword:
            return UserService.handle_category_removal(userid, category_name)
        else:
            return UserService.handle_keyword_removal(userid, category_name, keyword)


    @staticmethod
    def handle_category_removal(userid: int, category_name: str):
        user_manager = UserRepository()
        preferences_list = user_manager.fetch_user_preferences(userid)
        updated_preferences = remove_category_from_preferences(preferences_list, category_name)

        if len(updated_preferences) == len(preferences_list):
            return {"success": False, "message": f"Category '{category_name}' not found"}, 400

        user_manager.update_user_preferences(userid, updated_preferences)
        return {"success": True, "message": f"Category '{category_name}' removed"}, 200


    @staticmethod
    def handle_keyword_not_removed(keyword, category_name, keyword_removed):
        if not keyword_removed:
            return {
                "success": False,
                "message": f"Keyword '{keyword}' not found in category '{category_name}'"
            }, 400


    @staticmethod
    def handle_keyword_removal(userid: int, category_name: str, user_input_keywords):
        user_manager = UserRepository()
        preferences_list = user_manager.fetch_user_preferences(userid)

        updated_preferences, keyword_removed = remove_keywords_from_category(
            preferences_list, category_name, user_input_keywords
        )

        response = UserService.handle_keyword_not_removed(user_input_keywords, category_name, keyword_removed)
        if not response:
            user_manager.update_user_preferences(userid, updated_preferences)
            response = {
                "success": True,
                "message": f"Keyword '{user_input_keywords}' removed from category '{category_name}'"
            }, 200

        return response


    @staticmethod
    def get_article_details(article_id):
        article_manager = NewsArticleRepository()
        article = article_manager.find_by_id(article_id)
        article_manager.update_article_view_count(article_id)
        return {"success": True, "article": article.to_dict()}, 200
