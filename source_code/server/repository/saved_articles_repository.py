from database.database import db
from models.saved_article import SavedArticle
from typing import Optional, List
from interfaces.saved_articles import ISavedArticle


class SavedArticleRepository(ISavedArticle):
    def create(self, user_id: int, article_id: int) -> Optional[SavedArticle]:
        query = "INSERT INTO saved_articles (user_id, article_id) VALUES (%s, %s)"
        try:
            saved_id = db.execute_query(query, (user_id, article_id), commit=True)
            return SavedArticle(saved_id, user_id, article_id) if saved_id else None
        except Exception as e:
            if "Duplicate entry" in str(e):
                return None
            raise e


    def delete(self, user_id: int, article_id: int) -> bool:
        query = "DELETE FROM saved_articles WHERE user_id = %s AND article_id = %s"
        result = db.execute_query(query, (user_id, article_id), commit=True)
        return result is not None


    def is_article_saved(self, user_id: int, article_id: int) -> bool:
        query = "SELECT 1 FROM saved_articles WHERE user_id = %s AND article_id = %s"
        result = db.execute_query(query, (user_id, article_id), fetch_one=True)
        return result is not None


    def get_saved_articles_by_user(self, user_id: int) -> List[int]:
        query = "SELECT article_id FROM saved_articles WHERE user_id = %s"
        rows = db.execute_query(query, (user_id,), fetch_all=True)
        return [row['article_id'] for row in rows] if rows else []
