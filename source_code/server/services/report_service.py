from flask import current_app, url_for, jsonify
from repository.report_article_repository import ReportArticleRepository
from database.database import db
from services.email_format_service import EmailSender
from repository.category_repository import CategoryRepository

class ArticleReportService:
    def __init__(self):
        self.repo = ReportArticleRepository()
        self.threshold = 2

    def report_article(self, user_id, article_id, reason=""):
        article = self.repo.get_article_by_id(article_id)
        if not article:
            raise ValueError("Article not found")
        
        self.repo.add_report(user_id, article_id, reason)
        result, status_code = self.repo.increment_report_count(article_id)
        data = result.get_data(as_text=True) 
        print(data)
        # if article["report_count"]) + 1 >= self.threshold:
        #     self.repo.hide_article(article_id)
            
        self._send_admin_email(article_id, reason)
        
        return  data, status_code


    def _send_admin_email(self, article_id, reason):
        
        hide_link = url_for('admin_bp.hide_article', article_id=article_id,
                            token=current_app.config['SECRET_ADMIN_TOKEN'], _external=True)
        msg_body = f"""
            An article (ID: {article_id}) has been reported.

            Reason: {reason}

            Click below to hide the article:
            {hide_link}
            """
        
        email_send_manager = EmailSender(current_app.config)
        email_send_manager.send_email("deepanshu.p@intimetec.com","Article Reported", msg_body)
    
    
    def block_article_by_category(self, category_id):
        category_manager = CategoryRepository(db)
        admin_specified_category = category_manager.find_by_id(category_id)
        if not admin_specified_category:
            raise ValueError("Category Does not Exist.")
        
        category_manager.hideCategory(category_id)
    