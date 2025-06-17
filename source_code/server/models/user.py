from database.database import db
from werkzeug.security import generate_password_hash
from mysql.connector import Error
from datetime import datetime
import json

class User:
    def __init__(self, id, username, email, password_hash, role='user', created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at if created_at else datetime.now()

    @staticmethod
    def create(username, email, password, role='user'):
        query = "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)"
        hashed_password = generate_password_hash(password)
        try:
            user_id = db.execute_query(query, (username, email, hashed_password, role), commit=True)
            if user_id:
                return User(user_id, username, email, hashed_password, role, datetime.now())
            return None
        except Error as e:
            if e.errno == 1062: # Duplicate entry error code for MySQL
                print(f"User creation failed: Duplicate username or email for {username}/{email}")
            else:
                print(f"Error creating user: {e}")
            return None

    @staticmethod
    def find_by_username(username):
        query = "SELECT * FROM users WHERE username = %s"
        user_data = db.execute_query(query, (username,), fetch_one=True)
        if user_data:
            return User(**user_data)
        return None

    @staticmethod
    def find_by_email(email):
        query = "SELECT * FROM users WHERE email = %s"
        user_data = db.execute_query(query, (email,), fetch_one=True)
        if user_data:
            return User(**user_data)
        return None

    @staticmethod
    def find_by_id(user_id):
        query = "SELECT * FROM users WHERE id = %s"
        user_data = db.execute_query(query, (user_id,), fetch_one=True)
        if user_data:
            return User(**user_data)
        return None

    @staticmethod
    def is_admin(user_id):
        user = User.find_by_id(user_id)
        return user and user.role == 'admin'
    
    
    @staticmethod
    def remove_notification_keyword(userid, keyword):
        query = "SELECT category_preferences FROM user_notifications WHERE user_id = %s"
        result = db.execute_query(query, (userid,), fetch_one=True)
        if not result:
            return {"success": False, "message": "User not found"}, 404

        preferences = result.get('category_preferences') or '{}'
        try:
            preferences_list = json.loads(preferences)
        except json.JSONDecodeError:
            return {"success": False, "message": "Invalid JSON format in preferences"}, 500

        
        updated_preferences = [cat for cat in preferences_list if cat['name'].lower() != keyword.lower()]

        if len(updated_preferences) == len(preferences_list):
            return {"success": False, "message": f"Keyword '{keyword}' not found in category preferences"}, 400

        update_query = "UPDATE user_notifications SET category_preferences = %s WHERE user_id = %s"
        db.execute_query(update_query, (json.dumps(updated_preferences), userid), commit=True)

        return {"success": True, "message": f"Keyword '{keyword}' removed from preferences"}, 200