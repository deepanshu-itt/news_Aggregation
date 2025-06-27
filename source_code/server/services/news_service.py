from datetime import datetime, timedelta
from repository.news_article_repository import NewsArticleRepository
from repository.category_repository import CategoryRepository
from services.external_api_manager import ExternalAPIManager
from services.category_service import CategoryService
from services.notification_service import NotificationService
from repository.saved_articles_repository import SavedArticleRepository
from database.database import MySQLDatabaseConnection,Database 
from dto.news_article_dto import NewsArticleDto
from config import Config
from services.category_identifier import CategoryIdentifier


news_api_manager = ExternalAPIManager()
category_service = CategoryService()
notification_service = NotificationService()


class NewsService:
    
    @staticmethod
    def fetch_and_store_news(app_config):
        print(f"[{datetime.now()}] Starting news fetch and store process...")
        
        local_db, existing_categories, from_date_filter = NewsService._setup_dependencies()
        
        articles_from_apis = NewsService.fetch_articles_for_all_categories(existing_categories, from_date_filter)
        print(f"Total {len(articles_from_apis)} articles fetched.")
        
        new_articles_count = NewsService.store_articles(articles_from_apis, existing_categories, local_db)

        if new_articles_count > 0:
            print(f"[{datetime.now()}] Recorded system notification for {new_articles_count} new articles.")
            notification_service.send_daily_digests(app_config)
    
    
    @staticmethod
    def _setup_dependencies():
        mysql_connection = MySQLDatabaseConnection(Config)
        local_db = Database(mysql_connection)
        category_repository = CategoryRepository(db=local_db)
        
        existing_categories = {
            category.name.lower(): category.id
            for category in category_repository.get_all()
        }
        from_date_filter = datetime.now() - timedelta(days=1)
        return local_db, existing_categories, from_date_filter


    @staticmethod
    def fetch_articles_for_all_categories(existing_categories, from_date_filter):
        articles = []

        for category_name in existing_categories:
            category_label = category_name or "general_fetch"
            try:
                data = news_api_manager.get_news_from_all_sources({
                    "query": None,
                    "category": category_name,
                    "from_date": from_date_filter
                })
                articles.extend(data)
                print(f"Fetched {len(data)} articles for category: {category_label}")
            except Exception as error:
                print(f"News fetch for {category_label} failed: {error}")
        
        return articles

    
    @staticmethod
    def store_articles(articles, existing_categories, local_db):
        new_articles_count = 0
        category_repo = CategoryRepository(db=local_db)
        article_repo = NewsArticleRepository()

        for article in articles:
            if article_repo.find_by_url(article['url']):
                continue

            category_id = CategoryIdentifier.resolve_category_id(article, existing_categories, category_repo)

            published_time = NewsService.parse_published_time(article)

            new_article = article_repo.create(NewsArticleDto(
                title=article.get('title'),
                description=article.get('description'),
                url=article['url'],
                image_url=article.get('image_url'),
                published_at=published_time,
                source=article.get('source'),
                category_id=category_id,
                raw_data=article.get('raw_data', {})
            ))

            if new_article:
                new_articles_count += 1
        
        return new_articles_count

    
    @staticmethod
    def parse_published_time(article: dict):
        raw_data: dict = article.get('raw_data', {})
        time = (
            raw_data.get('published_at')
            or raw_data.get('publishedAt')
            or article.get('published_at')
            or article.get('publishedAt')
        )

        if time:
            artile_date_time = time.replace("Z", "").split(".")[0]
            try:
                return datetime.strptime(artile_date_time, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                print(f"Invalid date format: {artile_date_time}")
        print("Missing or malformed time:", article)
        return None


    @staticmethod
    def get_headlines_by_date_and_Category(article_filters, category_name: str = None):
        news_Article_manager = NewsArticleRepository()
        mysql_connection = MySQLDatabaseConnection(Config)
        local_db = Database(mysql_connection)
        category_repository = CategoryRepository(db = local_db)
        if category_name:
            category = category_repository.find_by_name(category_name.lower())
            article_filters["category_id"] = category.id
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
