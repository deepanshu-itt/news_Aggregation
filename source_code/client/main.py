from news_api import NewsAPIClient
from auth import Authentication
from admin import AdminMenu
from user import UserMenu

news_api_client = NewsAPIClient()
current_user = None

def set_current_user(user_data):
    global current_user
    current_user = user_data

def get_current_user():
    global current_user
    return current_user


def print_main_menu():
    print("\nWelcome to the News Aggregator application. Please choose the options below.")
    print("1. Login")
    print("2. Sign up")
    print("3. Exit")
    choice = input("Enter your option: ")
    return choice



def handle_user_type():
    print(f"Welcome, {current_user['username']}!")
    
    if current_user['role'] == 'admin':
        admin_menu = AdminMenu(news_api_client, get_current_user, set_current_user)
        admin_menu.run_menu()
    else:
        user_menu = UserMenu(news_api_client, get_current_user, set_current_user)
        user_menu.run_menu()

    return


def handle_user_login():
    user_data = Authentication.login(news_api_client)
    if user_data:
        set_current_user(user_data)
        handle_user_type()
    else:
        print("Login failed.")
        
    return


def main_menu():
    while True:
        choice = print_main_menu()
        if choice == '1':
           handle_user_login()
        elif choice == '2':
            Authentication.signup(news_api_client)
        elif choice == '3':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")



if __name__ == "__main__":
    main_menu()
