from flask import Blueprint, request, jsonify
from services.article_reaction import ArticleReactionService
from models.article_reaction import ArticleReactionModel
from database.database import db

article_reaction_bp = Blueprint('article_reaction', __name__)

def get_service():
    repo = ArticleReactionModel(db)
    return ArticleReactionService(repo)


@article_reaction_bp.route('/articles/<int:article_id>/react', methods=['POST'])
def react_to_article(article_id):
    service = get_service()
    data = request.get_json()
    user_id = request.headers.get('X-User-Id')
    reaction = data.get("reaction")

    try:
        service.react(user_id, article_id, reaction)
        return jsonify({"success": True,"message": f"{reaction} recorded successfully"}), 200
    except ValueError as ve:
        return jsonify({"success": False,"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"success": False,"error": "Something went wrong"}), 500

@article_reaction_bp.route('/articles/<int:article_id>/<string:reaction_type>', methods=['GET'])
def get_reaction_count(article_id, reaction_type):
    service = get_service()
    try:
        count = service.get_count(article_id, reaction_type)
        return jsonify({"success": True,"article_id": article_id, reaction_type: count}), 200
    except Exception as error:
        return jsonify({"success": False,"error": "Something went wrong"}), 500
