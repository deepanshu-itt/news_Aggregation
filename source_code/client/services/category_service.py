from news_api import NewsAPIClient
from dto.news_api_dto import NewsApiDto

class CategoryService:
    def __init__(self, api_client: NewsAPIClient, get_user):
        self.api_client = api_client
        self.get_user = get_user

    def create_category(self, category_name):
        get_saved_articles_dto = NewsApiDto(
            method='POST',
            endpoint='admin/categories',
            data= {'name': category_name},
            current_user=self.get_user()
        )
        return self.api_client.make_request(get_saved_articles_dto)

    
    def get_categories(self):
        get_saved_articles_dto = NewsApiDto(
            method='GET',
            endpoint='user/categories',
            current_user=self.get_user()
        )
        return self.api_client.make_request(get_saved_articles_dto)
    
    def hide_category_article(self, category_name):
        get_saved_articles_dto = NewsApiDto(
            method='POST',
            endpoint='admin/hide_category_article',
            data= {'name': category_name},
            current_user=self.get_user()
        )
        return self.api_client.make_request(get_saved_articles_dto)

    
    def unhide_category_article(self, category_name):
        get_saved_articles_dto = NewsApiDto(
            method='POST',
            endpoint='admin/unhide_category_article',
            data= {'name': category_name},
            current_user=self.get_user()
        )
        return self.api_client.make_request(get_saved_articles_dto)
