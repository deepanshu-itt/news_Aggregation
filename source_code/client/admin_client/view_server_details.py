from admin_client.base_Action import BaseAdminAction

class ViewServerDetailsAction(BaseAdminAction):

    def execute(self):
        print("\nList of external server details (API keys included):")
        response = self.__safe_execute(self.api_client.make_request, 'GET', 
                            'admin/external_servers/details', 
                            current_user=self.get_current_user())

        self.__is_valid_response(response)


    def __safe_execute(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print("An error occurred while executing the operation.")
            return None

    
    def __is_valid_response(self, response):
        if response and response.get('success'):
            self.__print_server_details(response)
        else:
            print("Failed to view server details.")
    
    
    def __print_server_details(self, response):
        
        for index, server in enumerate(response['servers']):
            print(f"{index+1}. {server['name']} - API Key: {server['api_key']}")
