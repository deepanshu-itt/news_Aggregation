from dto.api_request import APIRequest
import requests
from datetime import datetime
from typing import List, Optional
from interfaces.news_api import INewsAPI


class TheNewsAPICom(INewsAPI):
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key


    def fetch_news(self, request_data: APIRequest) -> List[dict]:
        url = f"{self.base_url}/all"
        params = self.__prepare_params(request_data)

        try:
            return self.__get_data_from_api(url,params)
        except requests.exceptions.RequestException:
            return []

    
    def __prepare_params(self,request_data: APIRequest):
        params = {
            "api_token": self.api_key,
            "language": "en",
            "limit": 5
        }
        if request_data.query:
            params["search"] = request_data.query
        if request_data.category:
            params["categories"] = request_data.category
        if request_data.from_date:
            params["published_after"] = request_data.from_date.strftime("%Y-%m-%d")
        if request_data.to_date:
            params["published_before"] = request_data.to_date.strftime("%Y-%m-%d")
        
        return params
    
    
    def __get_data_from_api(self,url, params):
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return [
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "image_url": article.get("image_url"),
                    "published_at": self._parse_date(article.get("published_at")),
                    "source": article.get("source", "Unknown"),
                    "category": self._extract_category(article),
                    "raw_data": article
                }
                for article in data.get("data", [])
        ]

    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except (TypeError, ValueError):
            return None

    def _extract_category(self, article: dict) -> str:
        categories = article.get("categories", [])
        return categories[0] if categories else "general"
