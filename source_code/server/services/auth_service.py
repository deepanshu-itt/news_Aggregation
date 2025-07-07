from repository.user_repository import UserRepository
from werkzeug.security import check_password_hash
from dto.user_dto import UserDto


class AuthService:
    
    @staticmethod
    def register_user(username, email, password):
        result = AuthService.check_details_validity(username, email, password)
        user_data = UserDto(username, email, password)
        if result is None:
            user_manager = UserRepository()
            user = user_manager.create(user_data)
            result = AuthService.check_user_exists(user)
            
        return result


    @staticmethod
    def login_user(email, password):
        user_manager = UserRepository()
        user = user_manager.find_by_email(email)
        result = None
        if not user or not check_password_hash(user.password_hash, password):
            result = {"success": False, "message": "Invalid email or password."}, 401
        else:
            result = {
                "success": True,
                "message": "Login successful.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
            }, 200
        return result

    
    @staticmethod
    def check_details_validity(username, email, password):
        if not username or not email or not password:
            return {"success": False, "message": "All fields are required."}, 400
        
        if "@" not in email or "." not in email:
            return {"success": False, "message": "Invalid email format."}, 400
        
        return None

    
    @staticmethod
    def check_user_exists(user):
        result = None
        if user:
            result = {"success": True, "message": "User registered successfully."}, 200
        else:
            result = {"success": False, "message": "Username or Email already exists."}, 409
        
        return result