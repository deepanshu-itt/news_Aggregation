from news_api import NewsAPIClient


class ArticleService:
    def __init__(self, api_client: NewsAPIClient, get_user):
        self.api_client = api_client
        self.get_user = get_user

    def get_saved_articles(self):
        return self.api_client.make_request('GET', 'user/articles/saved', current_user=self.get_user())


    def save_article(self, article_id):
        return self.api_client.make_request('POST', 'user/articles/save', 
                                {'article_id': article_id}, current_user=self.get_user())

    def delete_article(self, article_id):
        return self.api_client.make_request('POST', 'user/articles/unsave',
                                {'article_id': article_id}, current_user=self.get_user())

    def react_to_article(self, article_id, reaction):
        return self.api_client.make_request('POST', f'user/articles/{article_id}/react',
                                {'reaction': reaction}, current_user=self.get_user())
    

    def report_article(self, article_id, reason):
        return self.api_client.make_request('POST', f'user/articles/{article_id}/report',
                                {'reason': reason}, current_user=self.get_user())
