from flask import Blueprint, request, jsonify
from services.user_service import UserService
from services.news_service import NewsService
from repository.category_repository import CategoryRepository
from database.database import db
from routes.auth_routes import login_required


user_bp = Blueprint('user_bp', __name__)
user_service = UserService()


@user_bp.route('/news', methods=['GET'])
@login_required
def get_news():
    category_name = request.args.get('category')
    search_query = request.args.get('q')
    start = request.args.get('start_date')
    end =  request.args.get('end_date')
    user_id = request.headers.get('X-User-Id')
    article_filters = NewsService.create_article_filter(start, end, user_id)
    
    if search_query and start and end:
        articles = NewsService.search_articles_by_range(search_query, start, end)
    elif search_query:
        articles = NewsService.search_articles(search_query)
    elif start != None  and end != None and category_name != None :
        articles = NewsService.get_headlines_by_date_and_Category(article_filters, category_name = category_name)
    elif start != None  and end != None :
        articles = NewsService.get_headlines_by_date_and_Category(article_filters)
    else:
        print("Invalid data for searching Articles")
        jsonify({"success": False, "message": "Missing searching data."}), 403
    
    
    return jsonify({"success": True, "articles": [article.__dict__ for article in articles]}), 200


@user_bp.route('/categories', methods=['GET'])
@login_required
def get_categories():
    category_repository= CategoryRepository(db = db)
    categories = category_repository.get_all()
    return jsonify({"success": True, 
            "categories": [category.__dict__ for category in categories]}), 200


@user_bp.route('/article', methods=['GET'])
def get_article_details_route():
    print("ed")
    article_id = request.args.get('article_id')
    print("here is ", article_id)
    if not article_id:
        return jsonify({"success": False, "message": "Ärticle ID not specified"}), 200
    result, status_code = user_service.get_article_details(article_id)
    return jsonify(result), status_code
