from flask import current_app, url_for
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
        data, status_code = self.repo.increment_report_count(article_id)
        

        if article.get("report_count") + 1 >= self.threshold:
            self.repo.hide_article(article_id)
            self._update_admin_article_hide_email(article_id)

        else:
            self._send_hide_article_admin_email(article_id, reason)
        
        return  data, status_code


    def _send_hide_article_admin_email(self, article_id, reason):
        
        hide_link = url_for('admin_bp.hide_article', article_id=article_id,
                            token=current_app.config['SECRET_ADMIN_TOKEN'], _external=True)
        msg_body = f"""
            An article (ID: {article_id}) has been reported.

            Reason: {reason}

            Click below to hide the article:
            {hide_link}
            
            Thanks,
            """
        
        email_send_manager = EmailSender(current_app.config)
        email_send_manager.send_email("deepanshu.p@intimetec.com","Article Reported", msg_body)


    def _update_admin_article_hide_email(self, article_id, article_report_count):
        
        message_body = f"""
            An article (ID: {article_id}) Has been Blocked.

            Due to Article Reported limit ({article_report_count}) breached the article is automatically blocked for public view.
            
            Thanks,
            """
        
        email_send_manager = EmailSender(current_app.config)
        email_send_manager.send_email("deepanshu.p@intimetec.com","Article Reported", message_body)
    
    
    def block_article_by_category(self, category_name):
        category_manager = CategoryRepository(db)
        admin_specified_category = category_manager.find_by_name(category_name)
        if not admin_specified_category:
            raise ValueError("Category Does not Exist.")
        
        category_manager.hideCategory(admin_specified_category.id)
    
    
    def unblock_article_by_category(self, category_name):
        category_manager = CategoryRepository(db)
        admin_specified_category = category_manager.find_by_name(category_name)
        if not admin_specified_category:
            raise ValueError("Category Does not Exist.")
        
        category_manager.unhideCategory(admin_specified_category.id)
    
    
    def block_article_by_keyword(self, keyword):
        self.repo.hide_by_keyword(keyword)
