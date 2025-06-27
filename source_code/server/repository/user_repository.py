from database.database import db
from werkzeug.security import generate_password_hash
from mysql.connector import Error
from typing import Optional
from models.user import User
from interfaces.user import IUser
import json
from dto.cursor_dto import CursorDto


class UserRepository(IUser):
    
    def create(self, username: str, email: str, password: str, role: str = 'user') -> Optional[User]:
        hashed_password = generate_password_hash(password)
        query = "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)"
        cursor_params = CursorDto(query=query, params=(username, email, hashed_password, role), commit=True)
        result = db.execute_query(cursor_params)
        try:
            user_id = db.execute_query(cursor_params)
            return User(user_id, username, email, hashed_password, role) if user_id else None
        except Error as error:
            if error.errno == 1062:
                raise ValueError("Duplicate username or email")
            raise RuntimeError(f"Database error: {error}")


    def find_by_user_id(self, user_id: int) -> Optional[User]:
        query = "SELECT * FROM users WHERE id = %s"
        cursor_params = CursorDto(query=query, params=(user_id,), fetch_one=True)
        data = db.execute_query(cursor_params)
        return User(**data) if data else None


    def find_by_username(self, username: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE username = %s"
        cursor_params = CursorDto(query=query, params=(username,), fetch_one=True)
        data = db.execute_query(cursor_params)
        return User(**data) if data else None


    def find_by_email(self, email: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE email = %s"
        cursor_params = CursorDto(query=query, params=(email,), fetch_one=True)
        data = db.execute_query(cursor_params)
        return User(**data) if data else None


    def remove_notification_keyword(self, userid, category_name, keyword):
        result = None
        query = "SELECT category_preferences FROM user_notifications WHERE user_id = %s"
        cursor_params = CursorDto(query=query, params=(userid,), fetch_one=True)
        result = db.execute_query(cursor_params)
        
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
        cursor_params.query = update_query
        cursor_params.params = (json.dumps(updated_preferences), userid)
        cursor_params.commit = True
        cursor_params.fetch_one = False
        db.execute_query(cursor_params)

        return {"success": True, "message": f"Keyword '{keyword}' removed from preferences"}, 200