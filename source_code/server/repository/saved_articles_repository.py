from database.database import db
from models.saved_article import SavedArticle
from typing import Optional, List
from interfaces.saved_articles import ISavedArticle
from dto.cursor_dto import CursorDto
from repository.mysql_queries.saved_article_queries import (
    check_article_saved_query,
    create_saved_article_query,
    delete_saved_article_by_user_article_id_query,
    get_saved_article_by_user_query
)


class SavedArticleRepository(ISavedArticle):
    
    def create(self, user_id: int, article_id: int) -> Optional[SavedArticle]:
        result = None
        query = create_saved_article_query
        cursor_params = CursorDto(query=query, params=(user_id, article_id), commit=True)
        try:
            saved_id = db.execute_query(cursor_params)
            result = SavedArticle(saved_id, user_id, article_id) if saved_id else None
        except Exception as error:
            self.__check_error(error)
        return result


    def delete(self, user_id: int, article_id: int) -> bool:
        query = delete_saved_article_by_user_article_id_query
        cursor_params = CursorDto(query=query, params=(user_id, article_id), commit=True)
        result = db.execute_query(cursor_params)
        return result is not None


    def is_article_saved(self, user_id: int, article_id: int) -> bool:
        query = check_article_saved_query
        cursor_params = CursorDto(query=query, params=(user_id, article_id), fetch_one=True)
        result = db.execute_query(cursor_params)
        return result is not None


    def get_saved_articles_by_user(self, user_id: int) -> List[int]:
        query = get_saved_article_by_user_query
        cursor_params = CursorDto(query=query, params=(user_id,), fetch_all=True)
        rows = db.execute_query(cursor_params)
        return [row['article_id'] for row in rows] if rows else []
    
    
    def __check_error(error):
        if "Duplicate entry" in str(error):
            return None
        else:
            raise error
