import requests
import getpass
from news_api import NewsAPIClient
from dto.news_api_dto import NewsApiDto

class Authentication:
    def __init__(self):
        self.session = requests.Session()
    
    @staticmethod
    def login(api_client: NewsAPIClient):
        print("\n--- Login ---")
        email = Authentication.__get_valid_email()
        password = getpass.getpass("Enter your password: ")
        response = Authentication.use_login_api(email, password, api_client)

        return Authentication.get_user_from_response(response)


    @staticmethod
    def use_login_api(email, password, api_client: NewsAPIClient):
        login_dto = NewsApiDto(
            method='POST',
            endpoint='auth/login',
            data={'email': email, 'password': password}
        )
        return api_client.make_request(login_dto)
        
    
    @staticmethod
    def logout(set_current_user_callback):
        set_current_user_callback(None)
        print("Logged out successfully.")

    
    @staticmethod
    def signup(api_client):
        
        print("\n--- Sign Up ---")
        username = Authentication.__get_valid_username()
        email = Authentication.__get_valid_email()
        password = Authentication.__get_valid_password()

        signup_dto = NewsApiDto(
            method='POST',
            endpoint='auth/register',
            data={
            'username': username,
            'email': email,
            'password': password
        }
        )
        
        response = api_client.make_request(signup_dto )

        Authentication.__check_response(response)


    def __get_valid_username():
        username = None
        while True:
            username = input("Enter username (3-20 alphanumeric): ")
            if not (3 <= len(username) <= 20 and username.isalnum()):
                print("Username must be 3-20 alphanumeric characters.")
                continue
            break
        return username

    
    def __get_valid_email():
        email = None
        while True:
            email = input("Enter email: ")
            if not ("@" in email and "." in email):
                print("Invalid email format.")
                continue
            break
        
        return email

    
    def __get_valid_password():
        password = None
        while True:
            password = input("Enter password (min 8 chars, incl. upper, lower, digit, special): ")

            if len(password) < 8 or not any(character.isupper() for character in password) or \
            not any(character.islower() for character in password) or not any(character.isdigit() for character in password) or \
            not any(not character.isalnum() for character in password):
                print("Password must be at least 8 characters, contain uppercase, lowercase, digit, and special character.")
                continue
            break
        
        return password


    def __check_response(response):
        result = False
        if response and response.get('success'):
            print(response['message'])
            result = True
        else:
            print("Sign up failed.")
        
        return result


    def get_user_from_response(response):
        user = None
        if response and response.get('success'):
            print(response['message'])
            user = response['user']
        else:
            print("Login failed.")
        
        return user
