from datetime import datetime, timedelta
from models.user_notification import UserNotification
from repository.news_article_repository import NewsArticleRepository
from repository.email_notification_repository import EmailNotificationRepository
from repository.category_repository import CategoryRepository
from repository.user_notifications import UserNotificationRepository
from services.email_format_service import EmailSender
from dto.email_dto import EmailNotificationDto
from services.email_format_service import EmailContentFormatter
from services.article_filter import ArticleFilter
from database.database import MySQLDatabaseConnection,Database 
from config import Config


mysql_connection = MySQLDatabaseConnection(Config)
db = Database(mysql_connection)
class NotificationService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        self.category_repo = CategoryRepository(db=db)
        self.article_filter = ArticleFilter(self.category_repo)
        self.email_sender = None
        self.email_notification_repo = EmailNotificationRepository()
        self.user_notification_repo = UserNotificationRepository()
        self.news_article_repo = NewsArticleRepository()


    def send_digest_to_user(self, app_config, user_prefs: UserNotification, recent_articles):
        articles_for_user = self.article_filter.filter_articles(user_prefs, recent_articles)
        if not articles_for_user:
            print(f"No matching articles for user {user_prefs.email}.")
            return
        
        subject = "Your last 4 Hours News Updates!"
        body_lines = "Hi Geek, here are some recent news articles you might be interested in:\n\n"

        self.email_sender = EmailSender(app_config=app_config)
        articles_for_user = self.article_filter.filter_articles(user_prefs, recent_articles)
        body = EmailContentFormatter.build_email_content_from_articles(articles_for_user, body_lines)

        if self.email_sender.send_email(user_prefs.email, subject, body):
            article_ids = [article.id for article in articles_for_user]
            self.email_notification_repo.create(
                EmailNotificationDto(user_id=user_prefs.user_id, article_ids=article_ids, message=body)
            )
            print(f"Updates sent and recorded for user {user_prefs.email}.")
        else:
            print(f"Failed to send updates to user {user_prefs.email}.")


    def send_daily_digests(self, app_config):
        print(f"[{datetime.now()}] Starting updates notification process...")
        users_for_digest = self.user_notification_repo.get_users_for_daily_digest()

        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        recent_articles = self.news_article_repo.get_by_date_range(
            start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S")
        )

        if not recent_articles:
            print("No new articles to include in Quarterly updates.")
            return

        self.email_sender = EmailSender(app_config=app_config)
        for user_prefs in users_for_digest:
            self.send_digest_to_user(app_config, user_prefs, recent_articles)
        print(f"[{datetime.now()}] Quarterly updates notification process completed.")
