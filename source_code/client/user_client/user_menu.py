from user_client.handle_menu.headlines_menu import HeadlinesMenu
from user_client.handle_menu.saved_articles_menu import SavedArticlesMenu
from user_client.handle_menu.search_menu import SearchMenu
from user_client.handle_menu.notifications_menu import NotificationsMenu
from utils import print_menu
from datetime import datetime


class UserMenu:
    def __init__(self, api_client, get_current_user, set_current_user,
                 article_service, notification_service, user_service):
        self.api_client = api_client
        self.get_user = get_current_user
        self.set_user = set_current_user
        self.article_service = article_service
        self.notification_service = notification_service
        self.user_service = user_service

    def run_menu(self):
        response = True
        while response:
            self._welcome_user()
            choice = print_menu("Main Menu", [
                "Headlines", "Saved Articles", "Search", "Notifications", "Logout"
            ])

            if choice == '1':
                response = HeadlinesMenu(self).run()
            elif choice == '2':
                response = SavedArticlesMenu(self).run()
            elif choice == '3':
                response = SearchMenu(self).run()
            elif choice == '4':
                response = NotificationsMenu(self).run()
            elif choice == '5':
                self.user_service.logout()
                break
            else:
                print("Invalid option. Try again.")

    def _welcome_user(self):
        user = self.get_user()
        if user and 'username' in user:
            now = datetime.now()
            print(f"\nWelcome {user['username']}! Date: {now.strftime('%d-%b-%Y')} Time: {now.strftime('%I:%M%p')}")
        else:
            print("User not logged in.")
