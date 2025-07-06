from database.database import db
from werkzeug.security import generate_password_hash
from mysql.connector import Error
from typing import Optional
from models.user import User
from interfaces.user import IUser
import json
from dto.cursor_dto import CursorDto
from dto.user_dto import UserDto
from repository.mysql_queries.user_queries import (
    create_user_query,
    get_user_by_email,
    get_user_by_id_query,
    get_user_by_username,
    get_user_preferences_by_id_query,
    update_user_preferences_by_id_query
)


class UserRepository(IUser):
    
    def create(self, user_data: UserDto) -> Optional[User]:
        hashed_password = generate_password_hash(user_data.password)
        query = create_user_query
        cursor_params = CursorDto(query=query, params=(user_data.username, 
                                user_data.email, hashed_password, user_data.role), commit=True)
        
        try:
            user_id = db.execute_query(cursor_params)
            return User(user_id, user_data.username, user_data.email, hashed_password, user_data.role) if user_id else None
        except Error as error:
            if error.errno == 1062:
                raise ValueError("Duplicate username or email")
            raise RuntimeError(f"Database error: {error}")


    def find_by_user_id(self, user_id: int) -> Optional[User]:
        query = get_user_by_id_query 
        cursor_params = CursorDto(query=query, params=(user_id,), fetch_one=True)
        data = db.execute_query(cursor_params)
        return User(**data) if data else None


    def find_by_username(self, username: str) -> Optional[User]:
        query = get_user_by_username
        cursor_params = CursorDto(query=query, params=(username,), fetch_one=True)
        data = db.execute_query(cursor_params)
        return User(**data) if data else None


    def find_by_email(self, email: str) -> Optional[User]:
        query = get_user_by_email
        cursor_params = CursorDto(query=query, params=(email,), fetch_one=True)
        data = db.execute_query(cursor_params)
        return User(**data) if data else None



    def update_user_preferences(self, userid, updated_preferences):
        update_query = update_user_preferences_by_id_query
        cursor_params = CursorDto(
            query=update_query,
            params=(json.dumps(updated_preferences), userid),
            commit=True,
            fetch_one=False
        )
        db.execute_query(cursor_params)


    def fetch_user_preferences(self, userid):
        query = get_user_preferences_by_id_query
        cursor_params = CursorDto(query=query, params=(userid,), fetch_one=True)
        result: dict = db.execute_query(cursor_params)

        if not result:
            return None

        preferences = result.get('category_preferences') or '[]'

        try:
            return json.loads(preferences)
        except json.JSONDecodeError:
            return []
