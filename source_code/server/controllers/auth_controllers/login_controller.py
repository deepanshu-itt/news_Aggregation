from flask import jsonify, session
from services.auth_service import AuthService
from flask import request


def login():
    auth_service = AuthService()
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    result, status_code = auth_service.login_user(email, password)
    if result.get('success'):
        session['user_id'] = result['user']['id']
        session['username'] = result['user']['username']
        session['role'] = result['user']['role']
    else:
        print("no session\n")

    return jsonify(result), status_code
