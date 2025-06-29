from datetime import datetime
from auth import Authentication
from news_api import NewsAPIClient


class AdminMenu:
    def __init__(self, api_client: NewsAPIClient, get_current_user_callback, set_current_user_callback):
        self.api_client = api_client
        self.get_current_user = get_current_user_callback
        self.set_current_user = set_current_user_callback
    
    def _print_menu(self):
        print("\n--- Admin Menu ---")
        print("1. View list of external servers and status")
        print("2. View external server's details (incl. API key)")
        print("3. Update/Edit external server's details")
        print("4. Add new News Category")
        print("5. Hide Articles For Category")
        print("6. Unhide Articles For Category")
        print("7. Add Keybord to block articles")
        print("8. Logout")


    def run_menu(self):
        while True:
            self._print_menu()
            choice = input("Enter your option: ")

            if choice == '1':
                self._view_external_servers_status()
            elif choice == '2':
                self._view_external_server_details()
            elif choice == '3':
                self._update_external_server_details()
            elif choice == '4':
                self._add_news_category()
            elif choice == '5':
                self._hide_articles_by_category()
            elif choice == '6':
                self._unhide_articles_by_category()
            elif choice == '7':
                self._hide_articles_by_keywords()
            elif choice == '8':
                Authentication.logout(self.set_current_user)
                break
            else:
                print("Invalid option. Please try again.")


    def _view_external_servers_status(self):
        print("\nList of external servers:")
        response = self.api_client.make_request('GET', 'admin/external_servers', current_user=self.get_current_user())
        if self.__is_valid_response(response):
            self.__print_servers(response)
        
        else:
            print("Failed to retrieve server status.")

    
    def __is_valid_response(self, response):
        if response and response.get('success'):
            return True
        else:
            print("Invalid Response")

    
    def __print_servers(self, response):
        for index, server in enumerate(response['servers']):
            status_text = "Active" if server['status'] == 'active' else "Not Active"
            raw_date = server['last_accessed']
            formatted_date =self.__extract_formatted_date(raw_date)
            print(f"{index+1}. {server['name']} - {status_text} - last accessed: {formatted_date}")


    def __extract_formatted_date(self,raw_date="N/A"):
        try:
            parsed_date = datetime.strptime(raw_date, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = parsed_date.strftime("%d %b %Y")
        except ValueError:
            formatted_date = "Invalid Date"
        
        return formatted_date


    def _view_external_server_details(self):
        print("\nList of external server details (API keys included):")
        response = self.api_client.make_request('GET', 'admin/external_servers/details', current_user=self.get_current_user())
        
        if response and response.get('success'):
            for index, server in enumerate(response['servers']):
                print(f"{index+1}. {server['name']} - API Key: {server['api_key']}")
        else:
            print("Failed to retrieve server details.")


    def _update_external_server_details(self):
        print("\nUpdate/Edit the external server’s details")
        
        server_id = self._get_valid_server_id()

        payload = self._get_external_server_details()
        
        if not payload:
            print("No changes specified.")
            return

        response = self.api_client.make_request('PUT', f'admin/external_servers/{server_id}/status', payload, current_user=self.get_current_user())
        self._print_response(response, "Failed to update server details.")


    def _get_valid_server_id(self):
        try:
            server_id = None
            while(not server_id):
                server_id_str = input("Enter the external server ID: ")
                server_id = int(server_id_str)
        except ValueError:
            print("Invalid server ID. Please enter a number.")
            
        return server_id_str


    def _get_external_server_details(self):
        new_api_key = input("Enter the updated API key (leave blank for no change): ")
        new_status = input("Enter new status (active/inactive, leave blank for no change): ").lower()

        payload = {}
        if new_api_key:
            payload['api_key'] = new_api_key
        if new_status in ['active', 'inactive']:
            payload['status'] = new_status
        elif new_status:
            print("Invalid status. Must be 'active' or 'inactive'. Status not changed.")
        
        return payload


    def _add_news_category(self):
        print("\nAdd new News Category")
        category_name = self._get_user_input("Enter the Category Name:-")
        response = self.api_client.make_request('POST', 'admin/categories', 
                                {'name': category_name}, current_user=self.get_current_user())
        self._print_response(response, "Failed to add new category.")
        

    def _hide_articles_by_category(self):
        print("\nHide Articles By Category")
        category_name = self._get_user_input("Enter the Category Name:-")
        response = self.api_client.make_request('POST', f'admin/hide_category_article',
                                {'name': category_name}, current_user=self.get_current_user())
        self._print_response(response, "Failed to hide articles by category.")
    
    
    def _unhide_articles_by_category(self):
        print("\nUnHide Articles By Category")
        category_name = self._get_user_input("Enter the Category Name:-")
        response = self.api_client.make_request('POST', f'admin/unhide_category_article',
                                {'name': category_name}, current_user=self.get_current_user())
        self._print_response(response, "Failed to unhide articles by category.")
    
    
    def _hide_articles_by_keywords(self):
        print("\nHide Articles By Keywords")
        keyword= self._get_user_input("Enter the Keyword:-")
        response = self.api_client.make_request('POST', f'admin/hide_article/keywords',
                                {'keyword': keyword}, current_user=self.get_current_user())
        self._print_response(response, "Failed to add keyword")
        
    
    def _get_user_input(self, message):
        user_input = None
        user_input = input(f"{message}")
        return user_input


    def _print_response(self,response, operation):
        if response and response.get('success'):
            print(response['message'])
        else:
            print(operation)
