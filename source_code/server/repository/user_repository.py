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


    def remove_notification_keyword(self, userid, category_name: str, keyword=None):
        if not keyword:
            return self.__handle_category_removal(userid, category_name)
        else:
            return self.__handle_keyword_removal(userid, category_name, keyword)


    def __handle_category_removal(self, userid: int, category_name: str):
        preferences_list = self.__fetch_user_preferences(userid)
        updated_preferences = [
            category for category in preferences_list
            if category['name'].lower() != category_name.lower()
        ]

        if len(updated_preferences) == len(preferences_list):
            return {"success": False, "message": f"Category '{category_name}' not found"}, 400

        self.__update_user_preferences(userid, updated_preferences)
        return {"success": True, "message": f"Category '{category_name}' removed"}, 200


    def __handle_keyword_removal(self, userid: int, category_name: str, user_input_keywords):
        preferences_list = self.__fetch_user_preferences(userid)
        updated_preferences = []
        keyword_removed = False
        
        for category in preferences_list:
            if category['name'].lower() == category_name.lower():
                original_keywords_list = category.get('keywords', [])
                updated_keywords = [
                    keyword for keyword in original_keywords_list 
                    if keyword.lower() not in  user_input_keywords
                ]
                if len(updated_keywords) != len(original_keywords_list):
                    keyword_removed = True
                category['keywords'] = updated_keywords
            updated_preferences.append(category)

        response = self.__handle_keyword_not_removed(user_input_keywords, category_name, keyword_removed)
        if not response:
            self.__update_user_preferences(userid, updated_preferences)
            response = {
                "success": True,
                "message": f"Keyword '{user_input_keywords}' removed from category '{category_name}'"
            }, 200
        
        return response 


    def __update_user_preferences(self, userid, updated_preferences):
        update_query = update_user_preferences_by_id_query
        cursor_params = CursorDto(
            query=update_query,
            params=(json.dumps(updated_preferences), userid),
            commit=True,
            fetch_one=False
        )
        db.execute_query(cursor_params)


    def __fetch_user_preferences(self, userid):
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


    def __handle_keyword_not_removed(self, keyword, category_name, keyword_removed):
        if not keyword_removed:
            return {
                "success": False,
                "message": f"Keyword '{keyword}' not found in category '{category_name}'"
            }, 400
