from flask import Blueprint, request, jsonify
from services.user_service import UserService
from services.news_service import NewsService
from services.report_service import ArticleReportService
from repository.category_repository import CategoryRepository
from database.database import db
from routes.auth_routes import login_required


user_bp = Blueprint('user_bp', __name__)
user_service = UserService()


@user_bp.route('/notifications', methods=['GET'])
@login_required
def get_user_preferences():
    user_id = request.headers.get('X-User-Id')
    result, status_code = user_service.get_user_email_notifications(user_id)
    if result.get('success'):
        return jsonify({"success": True, "notifications": result.get("notifications")}), 200

    return jsonify(result), status_code


@user_bp.route('/userpreferences', methods=['GET'])
@login_required
def configure_user_preferences():
    user_id = request.headers.get('X-User-Id')
    result, status_code = user_service.get_user_profile(user_id)
    if result.get('success'):
        user = result.get("user")
        preferences = user.get("preferences")
        return jsonify({"success": True, "preferences": preferences}), 200

    return jsonify(result), status_code


@user_bp.route('/notifications', methods=['PUT'])
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


@user_bp.route('/articles/save', methods=['POST'])
@login_required
def save_article_route():
    user_id = request.headers.get('X-User-Id')
    data = request.get_json()
    article_id = data.get('article_id')
    if not article_id:
        return jsonify({"success": False, "message": "Article ID is required"}), 400
    result, status_code = user_service.save_article(user_id, article_id)
    
    if status_code == 409:
        return jsonify({"success": True, "message": "Article already saved."}), 200
    return jsonify(result), status_code


@user_bp.route('/articles/unsave', methods=['POST'])
@login_required
def unsave_article_route():
    user_id = request.headers.get('X-User-Id')
    data = request.get_json()
    article_id = data.get('article_id')

    if not article_id:
        return jsonify({"success": False, "message": "Article ID is required"}), 400

    result, status_code = user_service.unsave_article(user_id, article_id)
    return jsonify(result), status_code


@user_bp.route('/articles/saved', methods=['GET'])
@login_required
def get_user_saved_articles_route():

    user_id = request.headers.get('X-User-Id')
    result = user_service.get_user_saved_articles(user_id)
    return jsonify(result), 200



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
    return jsonify({"success": True, "categories": [category.__dict__ for category in categories]}), 200


@user_bp.route('/notifications', methods=['DELETE'])
@login_required
def delete_user_keyword():
    user_id = request.headers.get('X-User-Id')
    data = request.get_json()
    category_name = data.get('category_name') 
    keyword = data.get('keywords') if data else None

    result, status_code = user_service.remove_notification_keyword(user_id, category_name, keyword)

    return jsonify(result), status_code


@user_bp.route('/articles/<int:article_id>/report', methods=['POST'])
@login_required
def report_article(article_id):
    user_id = request.headers.get('X-User-Id')
    data = request.get_json()
    report_reason = data.get('reason') if data else "Not Specified"
    service = ArticleReportService()
    result, status_code = service.report_article(user_id, article_id, report_reason)
    return jsonify(result), status_code


@user_bp.route('/articles/<int:article_id>/unreport', methods=['POST'])
@login_required
def unreport_article(article_id):
    user_id = request.headers.get('X-User-Id')
    service = ArticleReportService()
    result, status_code = service.unreport_article(user_id, article_id)
    return jsonify(result), status_code


@user_bp.route('/article', methods=['GET'])
def get_article_details_route():
    print("ed")
    article_id = request.args.get('article_id')
    print("here is ", article_id)
    if not article_id:
        return jsonify({"success": False, "message": "Ärticle ID not specified"}), 200
    result, status_code = user_service.get_article_details(article_id)
    return jsonify(result), status_code
