from flask import Blueprint, request, jsonify
from services.user_service import UserService
from routes.auth_routes import login_required

user_preferences_bp = Blueprint('user_preferences_bp', __name__)
user_service = UserService()


@user_preferences_bp.route('/notifications', methods=['GET'])
@login_required
def get_user_preferences():
    user_id = request.headers.get('X-User-Id')
    result, status_code = user_service.get_user_email_notifications(user_id)
    if result.get('success'):
        return jsonify({"success": True, "notifications": result.get("notifications")}), 200

    return jsonify(result), status_code


@user_preferences_bp.route('/userpreferences', methods=['GET'])
@login_required
def configure_user_preferences():
    user_id = request.headers.get('X-User-Id')
    result, status_code = user_service.get_user_profile(user_id)
    if result.get('success'):
        user = result.get("user")
        preferences = user.get("preferences")
        return jsonify({"success": True, "preferences": preferences}), 200

    return jsonify(result), status_code


@user_preferences_bp.route('/notifications', methods=['PUT'])
@login_required
def update_user_preferences():
    user_id = request.headers.get('X-User-Id')
    data = request.get_json()
    category_preferences = data.get('keywords') or []
    category_name = data.get('category_name') 
    result, status_code = user_service.update_user_preferences(
        user_id, category_name, category_preferences
    )
    return jsonify(result), status_code


@user_preferences_bp.route('/notifications', methods=['DELETE'])
@login_required
def delete_user_keyword():
    user_id = request.headers.get('X-User-Id')
    data = request.get_json()
    category_name = data.get('category_name') 
    keyword = data.get('keywords') if data else None

    result, status_code = user_service.remove_notification_keyword(user_id, category_name, keyword)

    return jsonify(result), status_code