from database.database import db
from models.saved_article import SavedArticle
from typing import Optional, List
from interfaces.saved_articles import ISavedArticle
from dto.cursor_dto import CursorDto


class SavedArticleRepository(ISavedArticle):
    
    def create(self, user_id: int, article_id: int) -> Optional[SavedArticle]:
        result = None
        query = "INSERT IGNORE INTO saved_articles (user_id, article_id) VALUES (%s, %s)"
        cursor_params = CursorDto(query=query, params=(user_id, article_id), commit=True)
        try:
            saved_id = db.execute_query(cursor_params)
            result = SavedArticle(saved_id, user_id, article_id) if saved_id else None
        except Exception as error:
            self.__check_error(error)
        return result

    

    def delete(self, user_id: int, article_id: int) -> bool:
        query = "DELETE FROM saved_articles WHERE user_id = %s AND article_id = %s"
        cursor_params = CursorDto(query=query, params=(user_id, article_id), commit=True)
        result = db.execute_query(cursor_params)
        return result is not None


    def is_article_saved(self, user_id: int, article_id: int) -> bool:
        query = "SELECT 1 FROM saved_articles WHERE user_id = %s AND article_id = %s"
        cursor_params = CursorDto(query=query, params=(user_id, article_id), fetch_one=True)
        result = db.execute_query(cursor_params)
        return result is not None


    def get_saved_articles_by_user(self, user_id: int) -> List[int]:
        query = "SELECT article_id FROM saved_articles WHERE user_id = %s"
        cursor_params = CursorDto(query=query, params=(user_id,), fetch_all=True)
        rows = db.execute_query(cursor_params)
        return [row['article_id'] for row in rows] if rows else []
    
    
    def __check_error(error):
        if "Duplicate entry" in str(error):
            return None
        else:
            raise error
