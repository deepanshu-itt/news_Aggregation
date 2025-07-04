from interfaces.article_reaction import IArticleReaction


class ArticleReactionService:
    def __init__(self, repository: IArticleReaction):
        self.repo = repository


    def react(self, user_id: int, article_id: int, reaction: str):
        if reaction not in ("like", "dislike"):
            raise ValueError("Invalid reaction. Use 'like' or 'dislike'.")
        self.repo.upsert_reaction(user_id, article_id, reaction)


    def get_count(self, article_id: int, reaction: str) -> int:
        return self.repo.get_reaction_count(article_id, reaction)
