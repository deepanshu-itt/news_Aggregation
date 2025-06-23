from abc import ABC, abstractmethod

class IArticleReaction(ABC):
    @abstractmethod
    def upsert_reaction(self, user_id: int, article_id: int, reaction: str):
        pass

    @abstractmethod
    def get_reaction_count(self, article_id: int, reaction: str) -> int:
        pass
