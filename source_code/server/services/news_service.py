from datetime import datetime, date, timedelta
from repository.news_article_repository import NewsArticleRepository
from repository.category_repository import CategoryRepository
from services.external_api_manager import ExternalAPIManager
from services.category_service import CategoryService
from database.database import db
from dto.news_article_dto import NewsArticleDto
from dto.api_request import APIRequest


news_api_manager = ExternalAPIManager()
category_service = CategoryService()
# notification_service = NotificationService()


class NewsService:
    @staticmethod
    def fetch_and_store_news(app_config):
        print(f"[{datetime.now()}] Starting news fetch and store process...")
        category_repository = CategoryRepository(db = db)
        existing_categories = {c.name.lower(): c.id for c in category_repository.get_all()}
        articles_from_apis = []
        from_date_filter = datetime.now() - timedelta(hours=4)

        for cat_name in existing_categories:
            category_label = cat_name or "general_fetch"
            try:
                data = news_api_manager.get_news_from_all_sources(
                    app_config=app_config,
                    api_request_data = APIRequest(
                        category =cat_name,
                        from_date = from_date_filter
                    )
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

            if new_article:
                new_articles_count += 1


        print(f"[{datetime.now()}] Stored {new_articles_count} new articles.")
        


    @staticmethod
    def get_headlines_today(start_date =str(date.today()), end_date =str(date.today()), category_name = None):
        category_id = None
        news_Article_manager = NewsArticleRepository()
        category_repository= CategoryRepository(db = db)
        if category_name:
            category = category_repository.find_by_name(category_name)
            if category:
                category_id = category.id
        return news_Article_manager.get_by_date_and_category(start_date, end_date, category_id)
