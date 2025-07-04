from utils import print_menu, display_articles, get_valid_article_id
from services.article_service import ArticleService
from utils import display_article_information
from news_api import NewsAPIClient


class SavedArticlesMenu:
    def __init__(self, user_menu):
        self.article_service: ArticleService = user_menu.article_service
        self.user_service = user_menu.user_service
        self.api_client: NewsAPIClient = user_menu.api_client


    def run(self):
        print("\n--- Saved Articles ---")
        response = self.article_service.get_saved_articles()
        if not isinstance(response, list) or not response[0].get('success'):
            print("Failed to load saved articles.")
            return True

        display_articles(response[0].get('articles', []))
        return self.safe_execute(self._handle_saved_articles_menu)

  
    def _handle_saved_articles_menu(self):
        while True:
            choice = print_menu("Manage Saved Articles", ["Back", "Logout", "Delete Article", "View Article Details"])
            if choice == '1':
                return True
            elif choice == '2':
                self.user_service.logout()
                return False
            elif choice == '3':
                article_id = get_valid_article_id()
                if article_id:
                    result = self.article_service.delete_article(article_id)
                    print(result.get('message', "Failed to delete article."))
            elif choice == '4':
                self.safe_execute(self._handle_article_details)
            else:
                print("Invalid option.")


    def _handle_article_details(self):
        article_id = self.safe_execute(lambda: int(input("Enter the Article ID:- ")))
        if not article_id:
            return

        response = self.safe_execute(self.article_service.get_article_details, article_id)
        if response:
            self.safe_execute(self.__handle_article_details_response, response)

    
    def __handle_article_details_response(self, article_details_response):
        if article_details_response and article_details_response.get("success"):
            self.safe_execute(display_article_information, article_details_response.get("article"))
        else:
            print("No Article Information Available.")


    def safe_execute(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print("An unexpected error occurred.")
            return None
