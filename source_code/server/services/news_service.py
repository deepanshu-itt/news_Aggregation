from datetime import datetime, date, timedelta
from repository.news_article_repository import NewsArticleRepository
from repository.category_repository import CategoryRepository
from services.external_api_manager import ExternalAPIManager
from services.category_service import CategoryService
from services.notification_service import NotificationService
from repository.saved_articles_repository import SavedArticleRepository
from database.database import MySQLDatabaseConnection,Database 
from dto.news_article_dto import NewsArticleDto
from config import Config
from flask import session

news_api_manager = ExternalAPIManager()
category_service = CategoryService()
notification_service = NotificationService()


class NewsService:
    @staticmethod
    def fetch_and_store_news(app_config):
        print(f"[{datetime.now()}] Starting news fetch and store process...")
        mysql_connection = MySQLDatabaseConnection(Config)
        local_db = Database(mysql_connection)
        category_repository = CategoryRepository(db = local_db)
        existing_categories = {category.name.lower(): category.id for category in category_repository.get_all()}
        articles_from_apis = []
        from_date_filter = datetime.now() - timedelta(days=1)
        
        for category_name in existing_categories:
            category_label = category_name or "general_fetch"
            try:
                data = news_api_manager.get_news_from_all_sources(
                    app_config=app_config,
                    api_request_data = {
                        "query" : None,
                        "category" :category_name,
                        "from_date" : from_date_filter
                        
                    }
                )
                articles_from_apis.extend(data)
                print(f"Fetched {len(data)} articles for category: {category_label}" )
            except Exception as exc:
                print(f"News fetch for {category_label} failed: {exc}")

        print(f"Total {len(articles_from_apis)} articles fetched.")

        new_articles_count = 0
        news_Article_manager = NewsArticleRepository()
        for article_data in articles_from_apis:
            if news_Article_manager.find_by_url(article_data['url']):
                continue

            category_id = None
            if article_data.get('category'):
                cat_name_from_api = article_data['category'].lower()
                category_id = existing_categories.get(cat_name_from_api)
                if not category_id:
                    new_cat = category_repository.create(article_data['category'].capitalize())
                    if new_cat:
                        existing_categories[new_cat.name.lower()] = new_cat.id
                        category_id = new_cat.id
                        print(f"Dynamically added new category: {new_cat.name}")

            if category_id is None:
                category_id = category_service.identify_category_from_text(
                    article_data.get('title', '') or '',
                    article_data.get('description', '') or ''
                )
                if category_id is None:
                    category_id = existing_categories.get('general')
                    if category_id is None:
                        general_cat = category_repository.create('General')
                        if general_cat:
                            existing_categories['general'] = general_cat.id
                            category_id = general_cat.id
                            print(f"Dynamically added 'General' category.")
                        else:
                            print("Warning: Could not create 'General' category. Article might be stored without category.")
            
            raw_data = article_data.get('raw_data') or {}
            time = (
                raw_data.get('published_at')
                or raw_data.get('publishedAt')
                or article_data.get('published_at')
                or article_data.get('publishedAt')
            )
            if time:
                dt = time.replace("Z", "").split(".")[0]
                dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
                time = dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                print(article_data)

            new_article = news_Article_manager.create(
                NewsArticleDto(
                title=article_data.get('title'),
                description=article_data.get('description'),
                url=article_data['url'],
                image_url=article_data.get('image_url'),
                published_at = time,
                source=article_data.get('source'),
                category_id=category_id,
                raw_data=article_data.get('raw_data', {})
                )
            )
            print(new_articles_count)
            if new_article:
                new_articles_count += 1

        print(f"[{datetime.now()}] Stored {new_articles_count} new articles.")
        
        if new_articles_count > 0:
            print(f"[{datetime.now()}] Recorded system notification for {new_articles_count} new articles.")

            notification_service.send_daily_digests(app_config)


    # @staticmethod
    # def get_headlines_by_date(article_filters):
    #     news_Article_manager = NewsArticleRepository()
    #     article_filters = NewsService.create_article_filter(start_date, end_date)
    #     result = news_Article_manager.get_by_date_and_category(article_filters)
    #     return result

    
    
    @staticmethod
    def get_headlines_by_date_and_Category(article_filters, category_name = None):
        news_Article_manager = NewsArticleRepository()
        mysql_connection = MySQLDatabaseConnection(Config)
        local_db = Database(mysql_connection)
        category_repository = CategoryRepository(db = local_db)
        if category_name:
            category = category_repository.find_by_name(category_name.lower())
            article_filters["category_id"] = category.id
            # if category:
                
            #     article_filters = NewsService.create_article_filter(start_date, end_date, category.id)

        result = news_Article_manager.get_by_date_and_category(article_filters)
        return result

   
    
    @staticmethod
    def search_articles(query):
        news_Article_manager = NewsArticleRepository()
        return news_Article_manager.search_by_keyword(query)


    @staticmethod
    def save_article_for_user(user_id, article_id):
        news_Article_manager = NewsArticleRepository()
        saved_article_manager = SavedArticleRepository()
        if news_Article_manager.find_by_id(article_id):
            return saved_article_manager.create(user_id, article_id)
        return None
    
    
    @staticmethod
    def get_saved_articles_for_user(user_id):
        news_Article_manager = NewsArticleRepository()
        return news_Article_manager.get_saved_by_user(user_id)

    
    @staticmethod
    def create_article_filter(start_date, end_date, user_id):

        article_filters = {
            "start_date": start_date,
            "end_date": end_date,
            "user_id": user_id
        }
            
        return article_filters