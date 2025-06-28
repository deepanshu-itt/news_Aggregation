from utils import display_articles, get_date
from user_client.handle_menu.headlines_menu import HeadlinesMenu
from news_api import NewsAPIClient
from user_client.article_service import ArticleService


class SearchMenu:
    def __init__(self, user_menu):
        self.api_client: NewsAPIClient  = user_menu.api_client
        self.get_user = user_menu.get_user
        self.article_service: ArticleService = user_menu.article_service
        self.user_service = user_menu.user_service


    def run(self):
        print("\n--- Search News ---")
        user_query = input("Enter keyword(s): ").strip()
        if not user_query:
            print("Search query can't be empty.")
            return True

        start, end = get_date()
        params = {
            'q': user_query,
            'start_date': start.strftime('%Y-%m-%d'),
            'end_date': end.strftime('%Y-%m-%d')
        }

        response = self.api_client.make_request('GET', 'user/news', params=params, 
                                            current_user=self.get_user())
        
        if not response.get('success'):
            print("Search failed.")
            return True

        articles = response.get('articles', [])
        display_articles(articles)
        if articles:
            return HeadlinesMenu(self).run()
        else:
            print("No results found.")
            return True
