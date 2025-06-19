from flask import Blueprint, request, jsonify, session
from services.auth_service import AuthService
import functools


auth_bp = Blueprint('auth_bp', __name__)
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    result, status_code = auth_service.register_user(username, email, password)
    return jsonify(result), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    result, status_code = auth_service.login_user(email, password)
    if result.get('success'):
        session['user_id'] = result['user']['id']
        session['username'] = result['user']['username']
        session['role'] = result['user']['role']
        print(session)
        print("hi")
    else:
        print("no session\n")
        # os.environ['user_id'] =  str(result['user']['id'])
        # os.environ['username'] = result['user']['username']
        # os.environ['role'] = result['user']['role']
    return jsonify(result), status_code

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # os.environ['user_id'] = None
    # os.environ['username'] = None
    # os.environ['role'] = None
    session.clear() 
    return jsonify({"success": True, "message": "Logged out successfully."}), 200


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('X-User-Id') :
            return jsonify({"error": "Authentication Required", "message": "Please log in to access this resource."}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        print(session)
        if not request.headers.get('X-User-Id') :
            return jsonify({"error": "Authentication Required", "message": "Please log in to access this resource."}), 401
        if request.headers.get('X-User-Role') != 'admin':
            return jsonify({"error": "Forbidden", "message": "Admin access required."}), 403
        return f(*args, **kwargs)
    return decorated_function
