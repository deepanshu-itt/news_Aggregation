import json
from database.database import db
from models.news_article import NewsArticle
from interfaces.news_article import INewsArticleRepository
from datetime import datetime
from typing import List, Optional
from dto.news_article_dto import NewsArticleDto
class NewsArticleRepository(INewsArticleRepository):
    
    def _map_row_to_article(self, row) -> NewsArticle:
        if isinstance(row.get("raw_data"), str):
            try:
                row["raw_data"] = json.loads(row["raw_data"])
            except json.JSONDecodeError:
                row["raw_data"] = {}
        return NewsArticle(**row)


    def create(self, article: NewsArticleDto) -> Optional[NewsArticle]:
        query = """
        INSERT INTO news_articles (title, description, url, image_url, published_at, source, category_id, raw_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        raw_data_json = json.dumps(article.raw_data) if isinstance(article.raw_data, dict) else article.raw_data

        try:
            article_id = db.execute_query(query, (
                article.title, article.description, article.url, article.image_url,
                article.published_at, article.source, article.category_id, raw_data_json
            ), commit=True)
            
            article.id = article_id
            return article
        except Exception as error:
            print(f"Error creating news article: {error}")
            return None


    def find_by_url(self, url: str) -> Optional[NewsArticle]:
        query = "SELECT * FROM news_articles WHERE url = %s"
        row = db.execute_query(query, (url,), fetch_one=True)
        return self._map_row_to_article(row) if row else None


    def find_by_id(self, article_id: int) -> Optional[NewsArticle]:
        query = "SELECT * FROM news_articles WHERE id = %s"
        row = db.execute_query(query, (article_id,), fetch_one=True)
        return self._map_row_to_article(row) if row else None


    def get_articles(self, category_id=0, search_query="", limit=0, offset=0) -> List[NewsArticle]:
        sql = """
        SELECT na.*, c.name AS category_name
        FROM news_articles na
        JOIN categories c ON na.category_id = c.id
        WHERE 1=1
        """
        params = []
        if category_id:
            sql += " AND na.category_id = %s"
            params.append(category_id)
        if search_query:
            like = f"%{search_query}%"
            sql += " AND (na.title LIKE %s OR na.description LIKE %s OR na.raw_data LIKE %s)"
            params += [like, like, like]
        sql += " ORDER BY na.published_at DESC"
        if limit:
            sql += " LIMIT %s OFFSET %s"
            params += [limit, offset]

        rows = db.execute_query(sql, tuple(params), fetch_all=True)
        return [self._map_row_to_article(r) for r in rows] if rows else []

    def get_by_date_and_category(self, start_date, end_date, category_id=None, limit=0, offset=0) -> List[NewsArticle]:
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date.split(" ")[0], "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date.split(" ")[0], "%Y-%m-%d").date()

        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.max.time())

        query = """
        SELECT na.*, c.name AS category_name
        FROM news_articles na
        JOIN categories c ON na.category_id = c.id
        WHERE na.published_at BETWEEN %s AND %s
        """
        params = [start_dt, end_dt]

        if category_id:
            query += " AND na.category_id = %s"
            params.append(category_id)

        query += " ORDER BY na.published_at DESC"
        if limit:
            query += " LIMIT %s OFFSET %s"
            params += [limit, offset]

        rows = db.execute_query(query, tuple(params), fetch_all=True)
        return [self._map_row_to_article(r) for r in rows] if rows else []

    def search_by_keyword(self, keyword: str, limit=50, offset=0) -> List[NewsArticle]:
        like = f"%{keyword}%"
        query = """
        SELECT na.*, c.name AS category_name
        FROM news_articles na
        JOIN categories c ON na.category_id = c.id
        WHERE na.title LIKE %s OR na.description LIKE %s OR na.raw_data LIKE %s
        ORDER BY na.published_at DESC
        LIMIT %s OFFSET %s
        """
        params = (like, like, like, limit, offset)
        rows = db.execute_query(query, params, fetch_all=True)
        return [self._map_row_to_article(article) for article in rows] if rows else []

    def get_saved_by_user(self, user_id: int, limit=20, offset=0) -> List[NewsArticle]:
        query = """
        SELECT na.*, c.name AS category_name
        FROM saved_articles sa
        JOIN news_articles na ON sa.article_id = na.id
        JOIN categories c ON na.category_id = c.id
        WHERE sa.user_id = %s
        ORDER BY sa.saved_at DESC
        LIMIT %s OFFSET %s
        """
        rows = db.execute_query(query, (user_id, limit, offset), fetch_all=True)
        return [self._map_row_to_article(article) for article in rows] if rows else []
