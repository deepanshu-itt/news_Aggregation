import requests
from dto.news_api_dto import NewsApiDto
from dotenv import load_dotenv
import os

load_dotenv()


class NewsAPIClient:
    def __init__(self, base_url= os.getenv("BASE_URL")):
        self.base_url = base_url


    def make_request(self, request_data: NewsApiDto):

        url = f"{self.base_url}/{request_data.endpoint}"
        headers = {"Content-Type": "application/json"}

        if request_data.current_user:
            headers['X-User-Id'] = str(request_data.current_user['id'])
            headers['X-User-Role'] = request_data.current_user['role']

        return self.__handle_api_request(url , request_data, headers)
        
    
    
    def __handle_api_request(self, url, request_data: NewsApiDto, headers):
        response = None

        try:
            response = self.__make_api_call(url , request_data, headers)
            response.raise_for_status()
            response = response.json()
    
        except requests.exceptions.ConnectionError:
            print("Connection Error: Could not connect to the server. Is the server running?")
        except requests.exceptions.RequestException as error:
            print(f"API request failed: {error}")
    
        
        return response
    
    
    def __make_api_call(self, url, request_data: NewsApiDto, headers):

        response = None
        if request_data.method == 'GET':
            response = requests.get(url, headers=headers, params= request_data.params)
        elif request_data.method == 'POST':
            response = requests.post(url, json= request_data.data, headers=headers)
        elif request_data.method == 'PUT':
            response = requests.put(url, json=request_data.data, headers=headers)
        elif request_data.method == 'DELETE':
            response = requests.delete(url, json=request_data.data, headers=headers)
        else:
            print("Client Error: Invalid HTTP method.")
        return response 
