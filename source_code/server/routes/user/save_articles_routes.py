from services.save_article_service import SaveArticleService
from flask import Blueprint, request, jsonify
from routes.auth_routes import login_required


save_article_bp = Blueprint('save_article_bp', __name__)


@save_article_bp.route('/articles/save', methods=['POST'])
@login_required
def save_article_route():
    user_id = request.headers.get('X-User-Id')
    data = request.get_json()
    article_id = data.get('article_id')
    save_Article_manager = SaveArticleService()
    if not article_id:
        return jsonify({"success": False, "message": "Article ID is required"}), 400
    result, status_code = save_Article_manager.save_article(user_id, article_id)
    
    if status_code == 409:
        return jsonify({"success": True, "message": "Article already saved."}), 200
    return jsonify(result), status_code


@save_article_bp.route('/articles/unsave', methods=['POST'])
@login_required
def unsave_article_route():
    user_id = request.headers.get('X-User-Id')
    data = request.get_json()
    article_id = data.get('article_id')
    save_article_manager = SaveArticleService()
    if not article_id:
        return jsonify({"success": False, "message": "Article ID is required"}), 400

    result, status_code = save_article_manager.unsave_article(user_id, article_id)
    return jsonify(result), status_code


@save_article_bp.route('/articles/saved', methods=['GET'])
@login_required
def get_user_saved_articles_route():
    user_id = request.headers.get('X-User-Id')
    save_article_manager = SaveArticleService()
    result = save_article_manager.get_user_saved_articles(user_id)
    return jsonify(result), 200
