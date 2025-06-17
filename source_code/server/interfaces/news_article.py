from abc import ABC, abstractmethod
from typing import List, Optional
from models.news_article import NewsArticle


class INewsArticleRepository(ABC):


    @abstractmethod
    def create(self, article: NewsArticle) -> Optional[NewsArticle]: pass


    @abstractmethod
    def find_by_url(self, url: str) -> Optional[NewsArticle]: pass


    @abstractmethod
    def find_by_id(self, article_id: int) -> Optional[NewsArticle]: pass


    @abstractmethod
    def get_articles(self, category_id=None, search_query=None, limit=0, offset=0) -> List[NewsArticle]: pass


    @abstractmethod
    def get_by_date_and_category(self, start_date, end_date, category_id=None, limit=0, offset=0) -> List[NewsArticle]: pass


    @abstractmethod
    def search_by_keyword(self, keyword: str, limit=50, offset=0) -> List[NewsArticle]: pass


    @abstractmethod
    def get_saved_by_user(self, user_id: int, limit=20, offset=0) -> List[NewsArticle]: pass
