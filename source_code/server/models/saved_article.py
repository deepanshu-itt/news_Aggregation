from database.database import db
from datetime import datetime

class SavedArticle:
    def __init__(self, id, user_id, article_id, saved_at=None):
        self.id = id
        self.user_id = user_id
        self.article_id = article_id
        self.saved_at = saved_at if saved_at else datetime.now()

    @staticmethod
    def create(user_id, article_id):
        query = "INSERT INTO saved_articles (user_id, article_id) VALUES (%s, %s)"
        try:
            saved_id = db.execute_query(query, (user_id, article_id), commit=True)
            if saved_id:
                return SavedArticle(saved_id, user_id, article_id)
            return None
        except Exception as e:
            if "Duplicate entry" in str(e) and "user_id" in str(e) and "article_id" in str(e):
                print(f"Article {article_id} already saved by user {user_id}.")
            else:
                print(f"Error saving article: {e}")
            return None

    @staticmethod
    def delete(user_id, article_id):
        query = "DELETE FROM saved_articles WHERE user_id = %s AND article_id = %s"
        result = db.execute_query(query, (user_id, article_id), commit=True)
        return result is not None # Returns True if rows were affected

    @staticmethod
    def is_article_saved(user_id, article_id):
        query = "SELECT 1 FROM saved_articles WHERE user_id = %s AND article_id = %s"
        result = db.execute_query(query, (user_id, article_id), fetch_one=True)
        return result is not None

    @staticmethod
    def get_saved_articles_by_user(user_id):
        query = "SELECT article_id FROM saved_articles WHERE user_id = %s"
        article_ids = db.execute_query(query, (user_id,), fetch_all=True)
        return [item['article_id'] for item in article_ids] if article_ids else []