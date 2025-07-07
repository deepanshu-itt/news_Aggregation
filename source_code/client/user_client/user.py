from user_client.user_menu import UserMenu
from services.article_service import ArticleService
from services.notification_service import NotificationService
from auth import Authentication

class UserService:
    def __init__(self, api_client, get_user_callback, set_user_callback):
        self.api_client = api_client
        self.get_user = get_user_callback
        self.set_user = set_user_callback


    def logout(self):
        Authentication.logout(self.set_user)


    def run_menu(self):
        article_service = ArticleService(self.api_client, self.get_user)
        notification_service = NotificationService(self.api_client, self.get_user)

        user_menu = UserMenu(
            api_client=self.api_client,
            get_current_user=self.get_user,
            set_current_user=self.set_user,
            article_service=article_service,
            notification_service=notification_service,
            user_service=self
        )

        user_menu.run_menu()
