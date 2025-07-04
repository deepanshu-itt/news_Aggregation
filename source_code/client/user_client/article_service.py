from news_api import NewsAPIClient
from dto.news_api_dto import NewsApiDto

class ArticleService:
    def __init__(self, api_client: NewsAPIClient, get_user):
        self.api_client = api_client
        self.get_user = get_user

    def get_saved_articles(self):
        get_saved_articles_dto = NewsApiDto(
            method='GET',
            endpoint='user/articles/saved',
            current_user=self.get_user()
        )
        return self.api_client.make_request(get_saved_articles_dto)


    def save_article(self, article_id):
        save_article_dto = NewsApiDto(
            method='POST',
            endpoint='user/articles/save',
            data= {'article_id': article_id},
            current_user=self.get_user()
        )
        return self.api_client.make_request(save_article_dto)


    def delete_article(self, article_id):
        get_saved_articles_dto = NewsApiDto(
            method='POST',
            endpoint='user/articles/unsave',
            data={'article_id': article_id},
            current_user=self.get_user()
        )
        return self.api_client.make_request(get_saved_articles_dto)

    def react_to_article(self, article_id, reaction):
        react_to_article_dto = NewsApiDto(
            method='POST',
            endpoint=f'user/articles/{article_id}/react',
            data= {'reaction': reaction}, 
            current_user=self.get_user()
        )
        return self.api_client.make_request(react_to_article_dto)
    

    def report_article(self, article_id, reason):
        report_article_dto = NewsApiDto(
            method='POST',
            endpoint=f'user/articles/{article_id}/report',
            data={'reason': reason},
            current_user=self.get_user()
        )
        return self.api_client.make_request(report_article_dto)
    
    
    def get_article_details(self, article_id):
        get_article_details_dto = NewsApiDto(
            method='GET',
            endpoint='user/article',
            params={'article_id': article_id},
            current_user=self.get_user()
        )
        return self.api_client.make_request(get_article_details_dto)

