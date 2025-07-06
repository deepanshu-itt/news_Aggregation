from services.news_service import NewsService
from utils.serializers import serialize_articles
from repository.saved_articles_repository import SavedArticleRepository


class SaveArticleService:
    @staticmethod
    def save_article(user_id, article_id):
        success = NewsService.save_article_for_user(user_id, article_id)
        if success:
            return {"success": True, "message": "Article saved successfully."}, 200
        return {"success": False, "message": "Failed to save article or already saved."}, 409


    @staticmethod
    def unsave_article(user_id, article_id):
        save_article_maneger = SavedArticleRepository()
        success = save_article_maneger.delete(user_id, article_id)
        if success:
            return {"success": True, "message": "Article unsaved successfully."}, 200
        return {"success": False, "message": "Failed to unsave article."}, 404


    @staticmethod
    def get_user_saved_articles(user_id):
        articles = NewsService.get_saved_articles_for_user(user_id)
        return {"success": True, "articles": serialize_articles(articles)}, 200
