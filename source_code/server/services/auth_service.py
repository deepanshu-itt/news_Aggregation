# from models.user import User
from repository.user_repository import UserRepository
from werkzeug.security import check_password_hash

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if not username or not email or not password:
            return {"success": False, "message": "All fields are required."}, 400
        
        if "@" not in email or "." not in email:
            return {"success": False, "message": "Invalid email format."}, 400

        user_manager = UserRepository()
        user = user_manager.create(username, email, password)

        if user:
            return {"success": True, "message": "User registered successfully."}, 201
        else:
            return {"success": False, "message": "Username or Email already exists."}, 409

    @staticmethod
    def login_user(email, password):
        user_manager = UserRepository()
        user = user_manager.find_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            return {"success": False, "message": "Invalid email or password."}, 401
        
        return {"success": True, "message": "Login successful.",
                "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role}}, 200
