from repository.user_notifications import UserNotificationRepository
from repository.saved_articles_repository import SavedArticleRepository
from services.news_service import NewsService
from repository.email_notification_repository import EmailNotificationRepository
from repository.user_repository import UserRepository
from models.user import User

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
        already_data = user_notification_manager.find_by_user_id(user.id)
        category_found = False
        updated_preferences = []

        for category in already_data.category_preferences:
            if category['name'].lower() == category_name.lower():
                category_found = True
                existing_keywords = set(category.get('keywords', []))
                new_keywords = existing_keywords.union(set(category_preferences))
                category['keywords'] = list(new_keywords)
                updated_preferences.append(category)
            else:
                updated_preferences.append(category)

        if not category_found:
            new_entry = {
                "name": category_name,
                "enabled": True,
                "keywords": category_preferences
            }
            updated_preferences.append(new_entry)

        return user_notification_manager.create_or_update(
            user.id, user.email, updated_preferences
        )

    @staticmethod
    def remove_notification_keyword(user_id: int, category_name: str, keyword):
        user_manager = UserRepository()
        user =  user_manager.find_by_user_id(user_id)
        if not user:
            return {"success": False, "message": "User not found"}, 404

        return  user_manager.remove_notification_keyword(user.id, category_name, keyword)


    @staticmethod
    def save_article(user_id, article_id):
        success = NewsService.save_article_for_user(user_id, article_id)
        if success:
            return {"success": True, "message": "Article saved successfully."}, 200
        return {"success": False, "message": "Failed to save article or already saved."}, 409


    @staticmethod
    def unsave_article(user_id, article_id):
        save_article_maneger = SavedArticleRepository()
        success = save_article_maneger.delete(user_id, article_id)
        if success:
            return {"success": True, "message": "Article unsaved successfully."}, 200
        return {"success": False, "message": "Failed to unsave article."}, 404


    @staticmethod
    def get_user_saved_articles(user_id):
        articles = NewsService.get_saved_articles_for_user(user_id)
        return {"success": True, "articles": [single_article.__dict__ for single_article in articles]}, 200
    
