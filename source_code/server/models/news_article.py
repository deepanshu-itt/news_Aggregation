from database.database import db
from datetime import datetime


class NewsArticle:
    def __init__(self, title, description, url, image_url, published_at, source, category_id, id=None, category_name = None, raw_data=None, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.url = url
        self.image_url = image_url
        self.published_at = published_at
        self.source = source
        self.category_id = category_id
        self.category_name = category_name
        self.raw_data = raw_data
        self.created_at = created_at if created_at else datetime.now()

    # @staticmethod
    # def create(title, description, url, image_url, published_at, source, category_id, raw_data):
    #     query = """
    #     INSERT INTO news_articles (title, description, url, image_url, published_at, source, category_id, raw_data)
    #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    #     """
        
    #     raw_data_json = json.dumps(raw_data) if isinstance(raw_data, dict) else raw_data

    #     try:
    #         article_id = db.execute_query(query, (
    #             title, description, url, image_url, published_at, source, category_id, raw_data_json
    #         ), commit=True)
    #         if article_id:
    #             return NewsArticle(article_id, title, description, url, image_url, published_at, source, category_id, raw_data)
    #         return None
    #     except Exception as e:
    #         # Handle duplicate URL error specifically
    #         if "Duplicate entry" in str(e) and "'url'" in str(e):
    #             print(f"Skipping duplicate article: {url}")
    #         else:
    #             print(f"Error creating news article: {e}")
    #         return None

    # @staticmethod
    # def find_by_url(url):
    #     query = "SELECT * FROM news_articles WHERE url = %s"
    #     article_data = db.execute_query(query, (url,), fetch_one=True)
    #     if article_data:
    #         if isinstance(article_data.get('raw_data'), str):
    #             article_data['raw_data'] = json.loads(article_data['raw_data'])
    #         return NewsArticle(**article_data)
    #     return None
    
    # @staticmethod
    # def find_by_id(article_id):
    #     query = "SELECT * FROM news_articles WHERE id = %s"
    #     article_data = db.execute_query(query, (article_id,), fetch_one=True)

    #     if article_data:
    #         raw_data = article_data.get('raw_data')
    #         if isinstance(raw_data, str):
    #             try:
    #                 article_data['raw_data'] = json.loads(raw_data)
    #             except json.JSONDecodeError:
    #                 article_data['raw_data'] = {}

    #         return NewsArticle(**article_data)

    # @staticmethod
    # def get_articles(category_id = None , search_query = None, limit = 0, offset = 0):
        
    #     sql = """
    #     SELECT na.*, c.name AS category_name
    #     FROM news_articles na
    #     JOIN categories c ON na.category_id = c.id
    #     WHERE 1=1
    #     """
    #     params = []

    #     if category_id:
    #         sql += " AND na.category_id = %s"
    #         params.append(category_id)
    #     if search_query:
    #         sql += " AND (na.title LIKE %s OR na.description LIKE %s OR na.raw_data LIKE %s)"
    #         params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])

    #     if limit and offset:
    #         sql += " ORDER BY na.published_at DESC LIMIT %s OFFSET %s"
    #         params.extend([limit, offset])

    #     articles_data = db.execute_query(sql, tuple(params), fetch_all=True)
    #     if articles_data:
    #         return [NewsArticle(**article_data) for article_data in articles_data]
    #     return []
    

    
    # @staticmethod
    # def get_by_date_and_category(start_date:str, end_date:str, category_id=None, limit=0, offset=0):
    #     if isinstance(start_date, str):
    #         start_date = start_date.split(" ")[0]
    #         start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    #         end_date = end_date.split(" ")[0]
    #         end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    #     elif isinstance(start_date, datetime):
    #         start_date = start_date.date()
    #         end_date = end_date.date()
    #     start_datetime = datetime.combine(start_date, datetime.min.time()) 
    #     end_datetime = datetime.combine(end_date, datetime.max.time())   
    #     print(start_datetime, end_datetime)
    #     query = """
    #     SELECT na.*, c.name AS category_name
    #     FROM news_articles na
    #     JOIN categories c ON na.category_id = c.id
    #     WHERE na.published_at >= %s AND na.published_at <= %s
    #     """
    #     params = [start_datetime, end_datetime]

    #     if category_id is not None:
    #         query += " AND na.category_id = %s"
    #         params.append(category_id)

    #     query += " ORDER BY na.published_at DESC"
        
    #     if limit and offset:
    #         query+= "LIMIT %s OFFSET %s"
    #         params.extend([limit, offset])

    #     articles_data = db.execute_query(query, tuple(params), fetch_all=True)

    #     if articles_data:
    #         return [NewsArticle(**{k: v for k, v in article_data.items() if k != 'category_name'}) for article_data in articles_data]

    #     print("No data found for:", start_date, "to", end_date, "category:", category_id)
    #     return []


    # @staticmethod
    # def search_by_keyword(keyword, limit=50, offset=0):
    #     query = """
    #     SELECT na.*, c.name AS category_name
    #     FROM news_articles na
    #     JOIN categories c ON na.category_id = c.id
    #     WHERE na.title LIKE %s OR na.description LIKE %s OR na.raw_data LIKE %s
    #     ORDER BY na.published_at DESC LIMIT %s OFFSET %s
    #     """
    #     search_param = f"%{keyword}%"
    #     params = (search_param, search_param, search_param, limit, offset)
    #     articles_data = db.execute_query(query, params, fetch_all=True)
    #     if articles_data:
    #         return [NewsArticle(**data) for data in articles_data]
    #     return []

    # @staticmethod
    # def get_saved_by_user(user_id, limit=20, offset=0):
    #     query = """
    #     SELECT na.*, c.name AS category_name
    #     FROM saved_articles sa
    #     JOIN news_articles na ON sa.article_id = na.id
    #     JOIN categories c ON na.category_id = c.id
    #     WHERE sa.user_id = %s
    #     ORDER BY sa.saved_at DESC
    #     LIMIT %s OFFSET %s
    #     """
    #     params = (user_id, limit, offset)
    #     articles_data = db.execute_query(query, params, fetch_all=True)
    #     if articles_data:
    #         return [NewsArticle(**data) for data in articles_data]
    #     return []