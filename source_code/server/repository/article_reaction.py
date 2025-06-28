from interfaces.article_reaction import IArticleReaction
from database import database
from dto.cursor_dto import CursorDto


class ArticleReactionRepository(IArticleReaction):
    def __init__(self, database_connection: database):
        self._db = database_connection
        

    def upsert_reaction(self, user_id: int, article_id: int, reaction: str):
        query = """
        INSERT INTO article_reactions (user_id, article_id, reaction)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE reaction = VALUES(reaction), reacted_at = CURRENT_TIMESTAMP
        """
        cursor_params = CursorDto(query=query, params=(user_id, article_id, reaction), commit=True)
        try:
            self._db.execute_query(cursor_params)
        except Exception as error:
                print(f"Error creating category: {error}")


    def get_reaction_count(self, article_id: int, reaction: str) -> int:
        query = """
        SELECT COUNT(*) as count FROM article_reactions
        WHERE article_id = %s AND reaction = %s
        """
        cursor_params = CursorDto(query=query, params=(article_id, reaction), commit=True)
        try:
            return ArticleReactionRepository(**self._db.execute_query(cursor_params))
        except Exception as error:
            print(f"Error creating category: {error}")
