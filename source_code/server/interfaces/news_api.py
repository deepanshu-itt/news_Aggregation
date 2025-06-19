from abc import ABC, abstractmethod
from dto.api_request import APIRequest
from typing import List


class INewsAPI(ABC):
    @abstractmethod
    def fetch_news(self, request_data: APIRequest) -> List[dict]:
        pass
