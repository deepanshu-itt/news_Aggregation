import requests


class NewsAPIClient:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url


    def make_request(self, method, endpoint, data=None, params=None, current_user=None):

        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}

        if current_user:
            headers['X-User-Id'] = str(current_user['id'])
            headers['X-User-Role'] = current_user['role']

        return self.__handle_api_request(url , data, method, params, headers)
        
    
    
    def __handle_api_request(self, url , data, method, params, headers):
        response = None

        try:
            response = self.__make_api_call(url , data, method, params, headers)
            response.raise_for_status()
            response = response.json()
    
        except requests.exceptions.ConnectionError:
            print("Connection Error: Could not connect to the server. Is the server running?")
        except requests.exceptions.RequestException as error:
            print(f"API request failed: {error}")
    
        
        return response
    
    
    def __make_api_call(self,url , data, method, params, headers):

        response = None
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, json=data, headers=headers)
        else:
            print("Client Error: Invalid HTTP method.")
        return response 
