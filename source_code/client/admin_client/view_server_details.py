from admin_client.base_Action import BaseAdminAction
from services.external_servers_service import ExternalServersService


class ViewServerDetailsAction(BaseAdminAction):

    def execute(self):
        print("\nList of external server details (API keys included):")
        response = self.__get_server_details_service()
        self.__is_valid_response(response)


    
    def __get_server_details_service(self):
        external_server_service = ExternalServersService(self.api_client, self.get_current_user)
        return self.__safe_execute(external_server_service.get_server_details)


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
