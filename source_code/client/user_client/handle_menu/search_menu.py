from utils import display_articles, get_date
from news_api import NewsAPIClient
from services.article_service import ArticleService
from dto.news_api_dto import NewsApiDto
from user_client.base_user_action import IUserAction


class SearchMenu(IUserAction):
    def __init__(self, user_menu):
        self.api_client: NewsAPIClient  = user_menu.api_client
        self.get_user = user_menu.get_user
        self.article_service: ArticleService = user_menu.article_service
        self.user_service = user_menu.user_service


    def run(self):
        print("\n--- Search News ---")
        user_query = self.__get_user_query()
        start, end = get_date()
        
        params = {
            'q': user_query,
            'start_date': start.strftime('%Y-%m-%d'),
            'end_date': end.strftime('%Y-%m-%d')
        }

        response = self.__get_search_news_from_api(params)
        
        self.__handle_response(response)
        
        return True
        

    
    def __get_user_query(self):
        user_query = None
        while not user_query:
            user_query = input("Enter keyword(s): ").strip()
            if not user_query:
                print("Search query can't be empty.")
            else:
                return user_query
    
    
    def __get_search_news_from_api(self, params):
        get_search_news_dto = NewsApiDto(
            method='GET',
            endpoint='user/news',
            params=params,
            current_user=self.get_user()
        )
        return self.api_client.make_request(get_search_news_dto)

        
    def __handle_response(self, response):
        result = self.__is_article_exist(response)
        if result:
            articles = response.get('articles', [])
            display_articles(articles)
            
        return result

    
    def __is_article_exist(self, response):
        is_article_exist = True
        if not response.get('success'):
            print("Search failed.")
            is_article_exist = False
        elif not response.get('articles'):
            print("No Articles Found")
            is_article_exist = False
        
        return is_article_exist
