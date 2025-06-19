class Authentication:
    
    @staticmethod
    def login(api_client):
        print("\n--- Login ---")
        email = Authentication.__get_valid_email()
        password = input("Enter your password: ")
        response = api_client.make_request('POST', 'auth/login', {'email': email, 'password': password})
        Authentication.__check_response(response,"Login failed.")
        print(response)
        return response["user"]
        
    
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

        response = api_client.make_request('POST', 'auth/register', {
            'username': username,
            'email': email,
            'password': password
        })

        Authentication.__check_response(response,"Sign up failed.")


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

            if len(password) < 8 or not any(c.isupper() for c in password) or \
            not any(c.islower() for c in password) or not any(c.isdigit() for c in password) or \
            not any(not c.isalnum() for c in password):
                print("Password must be at least 8 characters, contain uppercase, lowercase, digit, and special character.")
                continue
            break
        
        return password


    def __check_response(response,operation):
        if response and response.get('success'):
            print(response['message'])
            return True
        else:
            print(operation)
            return False
