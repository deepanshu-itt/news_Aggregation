from utils import print_menu, display_articles, get_valid_article_id
from user_client.article_service import ArticleService


class SavedArticlesMenu:
    def __init__(self, user_menu):
        self.article_service: ArticleService = user_menu.article_service
        self.user_service = user_menu.user_service

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
            choice = print_menu("Manage Saved Articles", ["Back", "Logout", "Delete Article"])
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
            else:
                print("Invalid option.")

        
    def safe_execute(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print("An unexpected error occurred.")
            return None
