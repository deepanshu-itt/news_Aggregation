from flask import Blueprint, request, jsonify
from services.article_reaction import ArticleReactionService
from repository.article_reaction import ArticleReactionRepository

from database.database import db 


article_reaction_bp = Blueprint('article_reaction', __name__)

def get_service():
    repo = ArticleReactionRepository(db)
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
    except ValueError as error:
        print(error)
        return jsonify({"success": False,"error": str(error)}), 400
    except Exception:
        print(error)
        return jsonify({"success": False,"error": "Something went wrong"}), 500
