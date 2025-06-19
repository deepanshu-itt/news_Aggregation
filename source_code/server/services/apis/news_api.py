from dto.api_request import APIRequest
import requests
from datetime import datetime
from typing import List, Optional
from interfaces.news_api import INewsAPI

class NewsAPIOrg(INewsAPI):
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def fetch_news(self, request_data: APIRequest) -> List[dict]:
        url = f"{self.base_url}/top-headlines"
        params = self.__prepare_params(request_data)

        try:
            return self.__get_data_from_api(url,params)
        except requests.exceptions.RequestException:
            return []

    
    def __prepare_params(self,request_data: APIRequest):
        params = {
            "apiKey": self.api_key,
            "language": "en",
            "pageSize": 5
        }
        if request_data.query:
            params["q"] = request_data.query
        if request_data.category:
            params["category"] = request_data.category
        if request_data.from_date:
            params["from"] = request_data.from_date.isoformat()
        if request_data.to_date:
            params["to"] = request_data.to_date.isoformat()
        
        return params
    
    
    def __get_data_from_api(self,url,params,request_data: APIRequest):
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return [
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "image_url": article.get("urlToImage"),
                    "published_at": self._parse_date(article.get("publishedAt")),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "category": request_data.category,
                    "raw_data": article
                }
                for article in data.get("articles", [])
            ]

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except (TypeError, ValueError):
            return None
