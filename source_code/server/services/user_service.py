from repository.user_notifications import UserNotificationRepository
from repository.saved_articles_repository import SavedArticleRepository
from services.news_service import NewsService
from repository.email_notification_repository import EmailNotificationRepository
from repository.user_repository import UserRepository

class UserService:
    @staticmethod
    def get_user_profile(user_id):
        user_manager = UserRepository()
        user = user_manager.find_by_user_id(user_id)
        user_notification_manager = UserNotificationRepository()
        if user:
            
            prefs = user_notification_manager.find_by_user_id(user_id)
            prefs_data = {
                'email_enabled': prefs.email_enabled if prefs else True,
                'daily_digest_enabled': prefs.daily_digest_enabled if prefs else False,
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
                    "sent_at": email_notification.sent_at,
                    "category_id": email_notification.category_id
                }
                for email_notification in user_email_notifications
            ]
            return {"success": True, "notifications": data}, 200

        return {"success": True, "message": "No notifications found"}, 404


    @staticmethod
    def update_user_preferences(user_id, email_enabled, daily_digest_enabled, category_preferences):
        user_manager = UserRepository()
        user =user_manager.find_by_user_id(user_id)
        if not user:
            return {"success": False, "message": "User not found."}, 404

      
        user_notification_manager = UserNotificationRepository()
        
        
        already_data = user_notification_manager.find_by_user_id(user_id)

        user_input_set = {name.lower() for name in category_preferences}

        filtered_already_data = [
            item for item in already_data.category_preferences
            if item['name'].lower() not in user_input_set
        ]

        existing_names = {item['name'].lower() for item in already_data.category_preferences}
        new_entries = [
            {'name': name, 'enabled': True}
            for name in category_preferences
            if name.lower() not in existing_names
        ]

        updated_data = filtered_already_data + new_entries
    
        notification_prefs = user_notification_manager.create_or_update(
            user_id, user.email, email_enabled, daily_digest_enabled, updated_data
        )
        if notification_prefs:
            return {"success": True, "message": "Preferences updated successfully."}, 200
        return {"success": False, "message": "Failed to update preferences."}, 500


    @staticmethod
    def remove_notification_keyword(user_id, keyword):
        user_manager = UserRepository()
        user =  user_manager.find_by_user_id(user_id)
        if not user:
            return {"success": False, "message": "User not found"}, 404

        return  user_manager.remove_notification_keyword(user.id, keyword)


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
    
