from database.database import db
import json 

class UserNotification:
    def __init__(self, id, user_id, email_enabled, daily_digest_enabled, category_preferences, email):
        self.id = id
        self.user_id = user_id
        self.email_enabled = email_enabled
        self.daily_digest_enabled = daily_digest_enabled
        self.email = email
       
        self.category_preferences = category_preferences if category_preferences else []
    
    def __repr__(self):
        return f"<UserNotification user_id={self.user_id}, type={self.type}, category_id={self.category_id}, keyword={self.keyword}, enabled={self.enabled}>"

    @staticmethod
    def create_or_update(user_id, user_email, email_enabled=True, daily_digest_enabled=False, category_preferences=None):
        existing_prefs = UserNotification.find_by_user_id(user_id)
        prefs_json = json.dumps(category_preferences) if category_preferences else '[]'

        if existing_prefs:
            query = """
            UPDATE user_notifications
            SET email_enabled = %s, daily_digest_enabled = %s, category_preferences = %s
            WHERE user_id = %s
            """
            db.execute_query(query, (email_enabled, daily_digest_enabled, prefs_json, user_id), commit=True)
            return UserNotification(existing_prefs.id, user_id, email_enabled, daily_digest_enabled, category_preferences, user_email)
        
        else:
            query = """
            INSERT INTO user_notifications (user_id, email_enabled, daily_digest_enabled, category_preferences)
            VALUES (%s, %s, %s, %s)
            """
            notification_id = db.execute_query(query, (user_id, email_enabled, daily_digest_enabled, prefs_json), commit=True)
            if notification_id:
                return UserNotification(notification_id, user_id, email_enabled, daily_digest_enabled, category_preferences)
        
        return None

    @staticmethod
    def find_by_user_id(user_id):
        query = "SELECT * FROM user_notifications WHERE user_id = %s"
        data = db.execute_query(query, (user_id,), fetch_one=True)
        if data:
            if isinstance(data.get('category_preferences'), str):
                data['category_preferences'] = json.loads(data['category_preferences'])
            return UserNotification(**data)
        return None
    
    @staticmethod
    def get_users_for_daily_digest():
        query = "SELECT un.*, u.email FROM user_notifications un JOIN users u ON un.user_id = u.id WHERE daily_digest_enabled = TRUE AND email_enabled = TRUE"
        data = db.execute_query(query, fetch_all=True)
        if data:
            for row in data:
                if isinstance(row.get('category_preferences'), str):
                    row['category_preferences'] = json.loads(row['category_preferences'])
            
            return [UserNotification(**row) for row in data]
        return []
