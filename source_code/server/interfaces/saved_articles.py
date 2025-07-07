from abc import ABC, abstractmethod
from typing import Optional, List
from models.saved_article import SavedArticle


class ISavedArticle(ABC):
    @abstractmethod
    def create(self, user_id: int, article_id: int) -> Optional[SavedArticle]:
        pass

    @abstractmethod
    def delete(self, user_id: int, article_id: int) -> bool:
        pass

    @abstractmethod
    def is_article_saved(self, user_id: int, article_id: int) -> bool:
        pass

    @abstractmethod
    def get_saved_articles_by_user(self, user_id: int) -> List[int]:
        pass
