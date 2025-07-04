# import request

# def register():
#     data = request.get_json()
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')

#     result, status_code = auth_service.register_user(username, email, password)
#     return jsonify(result), status_code