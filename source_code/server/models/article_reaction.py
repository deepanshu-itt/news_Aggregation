from interfaces.article_reaction import IArticleReaction
from database import database


class ArticleReactionModel(IArticleReaction):
    def __init__(self, database_connection: database):
        self._db = database_connection
        

    def upsert_reaction(self, user_id: int, article_id: int, reaction: str):
        query = """
        INSERT INTO article_reactions (user_id, article_id, reaction)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE reaction = VALUES(reaction), reacted_at = CURRENT_TIMESTAMP
        """
        self._db.execute_query(query, (user_id, article_id, reaction), commit=True)

    def get_reaction_count(self, article_id: int, reaction: str) -> int:
        query = """
        SELECT COUNT(*) as count FROM article_reactions
        WHERE article_id = %s AND reaction = %s
        """
        # return Category(**data) if data else None
        return ArticleReactionModel(**self._db.execute_query(query, (article_id, reaction), commit=True))

