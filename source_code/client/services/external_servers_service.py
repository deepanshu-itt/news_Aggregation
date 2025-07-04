from news_api import NewsAPIClient
from dto.news_api_dto import NewsApiDto

class ExternalServersService:
    def __init__(self, api_client: NewsAPIClient, get_user):
        self.api_client = api_client
        self.get_user = get_user

    def update_server(self, server_id, payload):
        get_saved_articles_dto = NewsApiDto(
            method='PUT',
            endpoint=f'admin/external_servers/{server_id}/status',
            data= payload,
            current_user=self.get_user()
        )
        return self.api_client.make_request(get_saved_articles_dto)

    
    def get_server_details(self):
        get_saved_articles_dto = NewsApiDto(
            method='GET',
            endpoint='admin/external_servers/details',
            current_user=self.get_user()
        )
        return self.api_client.make_request(get_saved_articles_dto)