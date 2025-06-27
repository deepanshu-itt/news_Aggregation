from typing import List
from repository.mysql_external_server_repository import MySQLExternalServerRepository
from dto.api_request_dto import APIRequest
from services.apis.news_api import NewsAPIOrg
from services.apis.the_news_api import TheNewsAPICom
from interfaces.news_api import INewsAPI


class ExternalAPIManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.api_services = {}
        return cls._instance

    
    def load_external_servers(self):
        repository = MySQLExternalServerRepository()
        servers = repository.get_all()
        self.api_services = {}

        for server in servers:
            if server.status != "active":
                continue

            if server.name == "News API":
                self.api_services[server.name] = NewsAPIOrg(server.base_url, server.api_key)
            elif server.name == "The News API":
                self.api_services[server.name] = TheNewsAPICom(server.base_url, server.api_key)


    def get_news_from_all_sources(self, api_request_data: dict) -> List[dict]:
        if not self.api_services:
            self.load_external_servers()

        articles = []
        for name, service in self.api_services.items():
            result = self._fetch_and_process_news(name, service, api_request_data)
            if result:
                articles.extend(result)

        return articles


    def _fetch_and_process_news(self, name, service: INewsAPI, api_request_data: dict) -> List[dict]:
        try:
            request_data = self._build_api_request(service, api_request_data)
            result = service.fetch_news(request_data)
            self._update_last_accessed(name)
            return result
        except Exception:
            print(f"Can't Get News From External Server {name}")
            return []


    def _build_api_request(self, service: INewsAPI, api_request_data: dict) -> 'APIRequest':
        return APIRequest(
            base_url=service.base_url,
            api_key=service.api_key,
            query=api_request_data.get("query"),
            category=api_request_data.get("category"),
            from_date=api_request_data.get("from_date"),
            to_date=api_request_data.get("to_date")
        )


    def _update_last_accessed(self, server_name: str):
        repository = MySQLExternalServerRepository()
        config = next((server_details for server_details in repository.get_all() if server_details.name == server_name), None)
        if config:
            repository.update_last_accessed(config.id)
