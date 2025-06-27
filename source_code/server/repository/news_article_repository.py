import json
from database.database import db
from models.news_article import NewsArticle
from interfaces.news_article import INewsArticleRepository
from datetime import datetime
from typing import List, Optional
from dto.news_article_dto import NewsArticleDto
from dto.cursor_dto import CursorDto
from repository.mysql_queries.news_article_queries import create_news_article_query


class NewsArticleRepository(INewsArticleRepository):

    def _map_row_to_article(self, row) -> NewsArticle:
        if isinstance(row.get("raw_data"), str):
            try:
                row["raw_data"] = json.loads(row["raw_data"])
            except json.JSONDecodeError:
                row["raw_data"] = {}
        return NewsArticle(**row)


    def create(self, article: NewsArticleDto) -> Optional[NewsArticle]:
        raw_data_json = json.dumps(article.raw_data) if isinstance(article.raw_data, dict) else article.raw_data
        result = None
        try:
            cursor_params = CursorDto(query=create_news_article_query, params=(
                article.title, article.description, article.url, article.image_url,
                article.published_at, article.source, article.category_id, raw_data_json
            ), commit=True)
            
            article_id = db.execute_query(cursor_params)
            
            article.id = article_id
        
            self.hide_by_category_table()
            self.hide_by_keyword_table()

            result = article
        
        except Exception as error:
            print(f"Error creating news article: {error}")
        
        return result


    def find_by_url(self, url: str) -> Optional[NewsArticle]:
        query = "SELECT * FROM news_articles WHERE url = %s"
        cursor_params = CursorDto(query=query, params=(url,), fetch_one=True)
        row = db.execute_query(cursor_params)
        return self._map_row_to_article(row) if row else None


    def find_by_id(self, article_id: int) -> Optional[NewsArticle]:
        query = "SELECT * FROM news_articles WHERE id = %s"
        cursor_params = CursorDto(query=query, params=(article_id,), fetch_one=True)
        row = db.execute_query(cursor_params)
        return self._map_row_to_article(row) if row else None


    def get_articles(self, category_id=None, search_query=None) -> List[NewsArticle]:
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
        cursor_params = CursorDto(query= sql, params=tuple(params), fetch_all=True)
        rows = db.execute_query(cursor_params)
        return [self._map_row_to_article(row) for row in rows] if rows else []


    def get_by_date_range(self, start_date, end_date) -> List[NewsArticle]:
        
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date.split(" ")[0], "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date.split(" ")[0], "%Y-%m-%d").date()

        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.max.time())

        query = """
            SELECT 
                na.*, 
                c.name AS category_name,
                COALESCE(SUM(ar.reaction = 'like'), 0) AS like_count,
                COALESCE(SUM(ar.reaction = 'dislike'), 0) AS dislike_count
            FROM news_articles na
            JOIN categories c ON na.category_id = c.id
            LEFT JOIN article_reactions ar ON na.id = ar.article_id
            WHERE na.is_hidden != 1 AND na.published_at BETWEEN %s AND %s
        """
        
        params = [start_dt, end_dt]

        query += """
            GROUP BY na.id 
            ORDER BY na.published_at DESC
        """
        cursor_params = CursorDto(query=query, params=tuple(params), fetch_all=True)
        rows = db.execute_query(cursor_params)
        return [self._map_row_to_article(rows) for rows in rows] if rows else []
    
    

    def search_by_keyword(self, keyword: str) -> List[NewsArticle]:
        like = f"%{keyword}%"
        query = """
        SELECT 
            na.*, 
            c.name AS category_name,
            COALESCE(SUM(ar.reaction = 'like'), 0) AS like_count,
            COALESCE(SUM(ar.reaction = 'dislike'), 0) AS dislike_count
        FROM news_articles na
        JOIN categories c ON na.category_id = c.id
        LEFT JOIN article_reactions ar ON na.id = ar.article_id
        WHERE na.is_hidden != 1 AND na.title LIKE %s OR na.description LIKE %s OR na.raw_data LIKE %s
        GROUP BY na.id
        ORDER BY na.published_at DESC
        """
        params = (like, like, like)
        cursor_params = CursorDto(query=query, params=params, fetch_all=True)
        rows = db.execute_query(cursor_params)
        return [self._map_row_to_article(rows) for rows in rows] if rows else []


    def get_saved_by_user(self, user_id: int) -> List[NewsArticle]:
        query = """
        SELECT 
            na.*, 
            c.name AS category_name,
            COALESCE(SUM(ar.reaction = 'like'), 0) AS like_count,
            COALESCE(SUM(ar.reaction = 'dislike'), 0) AS dislike_count
        FROM saved_articles sa
        JOIN news_articles na ON sa.article_id = na.id
        JOIN categories c ON na.category_id = c.id
        LEFT JOIN article_reactions ar ON na.id = ar.article_id
        WHERE na.is_hidden != 1 AND sa.user_id = %s 
        GROUP BY na.id
        ORDER BY sa.saved_at DESC
        """
        params = (user_id,)
        cursor_params = CursorDto(query=query, params=params, fetch_all=True)
        rows = db.execute_query(cursor_params)
        return [self._map_row_to_article(r) for r in rows] if rows else []


    def hide_by_keyword_table(self):
        query = """UPDATE news_articles
                    SET is_hidden = 1
                    WHERE EXISTS (
                        SELECT 1
                        FROM article_filters
                        WHERE news_articles.title LIKE CONCAT('%', article_filters.keyword, '%')
                    )"""
        cursor_params = CursorDto(query=query,fetch_one=True)
        db.execute_query(cursor_params)


    def hide_by_category_table(self):

        query = """ UPDATE news_articles na
                    JOIN categories c ON na.category_id = c.id
                    SET na.is_hidden = 1
                    WHERE c.is_hidden = 1
                """
        cursor_params = CursorDto(query=query, fetch_one=True)
        db.execute_query(cursor_params)

    
    def get_by_date_and_category(self, filters: dict) -> List[NewsArticle]:
        start_dt, end_dt = self._normalize_date_range(filters["start_date"], filters["end_date"])
        user_id = filters["user_id"]
        category_id = filters.get("category_id")

        query = """
            SELECT 
                na.*, 
                c.name AS category_name,
                COALESCE(SUM(ar.reaction = 'like'), 0) AS like_count,
                COALESCE(SUM(ar.reaction = 'dislike'), 0) AS dislike_count,
                (
                    CASE WHEN JSON_CONTAINS(un.category_preferences, JSON_QUOTE(c.name)) THEN 3 ELSE 0 END
                    +
                    CASE 
                        WHEN JSON_CONTAINS(un.category_preferences, JSON_QUOTE(c.name)) 
                            AND (na.title LIKE CONCAT('%', c.name, '%') 
                            OR na.description LIKE CONCAT('%', c.name, '%')) THEN 2
                        ELSE 0 
                    END
                    +
                    CASE WHEN sa.article_id IS NOT NULL THEN 2 ELSE 0 END
                    +
                    CASE WHEN ar_filter.article_id IS NOT NULL THEN 1 ELSE 0 END
                ) AS relevance_score

            FROM news_articles na
            JOIN categories c ON na.category_id = c.id
            LEFT JOIN article_reactions ar ON na.id = ar.article_id
            LEFT JOIN user_notifications un ON un.user_id = %s
            LEFT JOIN saved_articles sa ON sa.article_id = na.id AND sa.user_id = %s
            LEFT JOIN article_reactions ar_filter ON ar_filter.article_id = na.id AND ar_filter.user_id = %s AND ar_filter.reaction = 'like'

            WHERE na.is_hidden != 1 AND na.published_at BETWEEN %s AND %s
        """

        params = [user_id, user_id, user_id, start_dt, end_dt]

        if category_id:
            query += " AND na.category_id = %s"
            params.append(category_id)

        query += """
            GROUP BY na.id
            ORDER BY relevance_score DESC, na.published_at DESC
        """
        cursor_params = CursorDto(query=query, params=tuple(params), fetch_all=True)
        rows = db.execute_query(cursor_params)

        if rows:
            for row in rows:
                row.pop('relevance_score', None)
            return [self._map_row_to_article(row) for row in rows]
        return []


    def _normalize_date_range(self, start_date, end_date):
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date.split(" ")[0], "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date.split(" ")[0], "%Y-%m-%d").date()

        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.max.time())
        return start_dt, end_dt

    