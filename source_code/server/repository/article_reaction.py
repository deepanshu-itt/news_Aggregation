from interfaces.article_reaction import IArticleReaction
from database import database
from dto.cursor_dto import CursorDto
from repository.mysql_queries.article_reaction_queries import(
    upsert_reaction_query, get_reaction_count_query)


class ArticleReactionRepository(IArticleReaction):
    def __init__(self, database_connection: database):
        self._db = database_connection
        

    def upsert_reaction(self, user_id: int, article_id: int, reaction: str):
        cursor_params = CursorDto(query=upsert_reaction_query, params=(user_id, article_id, reaction), commit=True)
        try:
            self._db.execute_query(cursor_params)
        except Exception as error:
                print(f"Error creating category: {error}")


    def get_reaction_count(self, article_id: int, reaction: str) -> int:
        cursor_params = CursorDto(query=get_reaction_count_query, params=(article_id, reaction), commit=True)
        try:
            return ArticleReactionRepository(**self._db.execute_query(cursor_params))
        except Exception as error:
            print(f"Error creating category: {error}")
