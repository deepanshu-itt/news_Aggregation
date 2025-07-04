from auth import Authentication
from news_api import NewsAPIClient

from admin_client.view_servers import ViewServersAction
from admin_client.view_server_details import ViewServerDetailsAction
from admin_client.update_server import UpdateServerAction
from admin_client.add_category import AddCategoryAction
from admin_client.hide_article_by_category import HideArticlesByCategoryAction
from admin_client.unhide_articles_by_category import UnhideArticlesByCategoryAction
from admin_client.hide_articles_by_keyword import HideArticlesByKeywordsAction
from utils import clear_console


class AdminMenu:
    def __init__(self, api_client: NewsAPIClient, get_current_user_callback, set_current_user_callback):
        self.api_client = api_client
        self.get_current_user = get_current_user_callback
        self.set_current_user = set_current_user_callback


    def _print_menu(self):
        print("\n--- Admin Menu ---")
        print("1. View list of external servers and status")
        print("2. View external server's details (incl. API key)")
        print("3. Update/Edit external server's details")
        print("4. Add new News Category")
        print("5. Hide Articles For Category")
        print("6. Unhide Articles For Category")
        print("7. Add Keyword to block articles")
        print("8. Logout")


    def run_menu(self):
        while True:
            self._print_menu()
            choice = input("Enter your option: ")

            if choice == '1':
                ViewServersAction(self.api_client, self.get_current_user).execute()
            elif choice == '2':
                ViewServerDetailsAction(self.api_client, self.get_current_user).execute()
            elif choice == '3':
                UpdateServerAction(self.api_client, self.get_current_user).execute()
            elif choice == '4':
                AddCategoryAction(self.api_client, self.get_current_user).execute()
            elif choice == '5':
                HideArticlesByCategoryAction(self.api_client, self.get_current_user).execute()
            elif choice == '6':
                UnhideArticlesByCategoryAction(self.api_client, self.get_current_user).execute()
            elif choice == '7':
                HideArticlesByKeywordsAction(self.api_client, self.get_current_user).execute()
            elif choice == '8':
                Authentication.logout(self.set_current_user)
                break
            else:
                print("Invalid option. Please try again.")
