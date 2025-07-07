from services.report_service import ArticleReportService
from flask import Blueprint, request, jsonify
from routes.auth_routes import login_required


report_article_bp = Blueprint('report_article_bp', __name__)

@report_article_bp.route('/articles/<int:article_id>/report', methods=['POST'])
@login_required
def report_article(article_id):
    user_id = request.headers.get('X-User-Id')
    data = request.get_json()
    report_reason = data.get('reason') if data else "Not Specified"
    service = ArticleReportService()
    result, status_code = service.report_article(user_id, article_id, report_reason)
    response = jsonify({"success": True, "message": result})
    return response, status_code


@report_article_bp.route('/articles/<int:article_id>/unreport', methods=['POST'])
@login_required
def unreport_article(article_id):
    user_id = request.headers.get('X-User-Id')
    service = ArticleReportService()
    result, status_code = service.unreport_article(user_id, article_id)
    response = jsonify({"success": True, "message": result})
    return response, status_code
