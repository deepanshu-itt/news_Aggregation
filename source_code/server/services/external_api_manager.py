from typing import List
from repository.mysql_external_server_repository import MySQLExternalServerRepository
from dto.api_request import APIRequest
from services.apis.news_api import NewsAPIOrg
from services.apis.the_news_api import TheNewsAPICom

class ExternalAPIManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.api_services = {}
        return cls._instance

    def reload_api_configs(self, app_config):
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

    def get_news_from_all_sources(self, app_config, api_request_data: dict) -> List[dict]:
        if not self.api_services:
            self.reload_api_configs(app_config)

        articles = []
        repository = MySQLExternalServerRepository()

        for name, service in self.api_services.items():
            try:
                request_data = APIRequest(
                    base_url=service.base_url,
                    api_key=service.api_key,
                    query=api_request_data.get("query"),
                    category=api_request_data.get("category"),
                    from_date=api_request_data.get("from_date"),
                    to_date=api_request_data.get("to_date")
                )
                result = service.fetch_news(request_data)
                articles.extend(result)
                config = next((s for s in repository.get_all() if s.name == name), None)
                if config:
                    repository.update_last_accessed(config.id)
            except Exception:
                continue

        return articles
