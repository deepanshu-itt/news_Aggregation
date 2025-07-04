from datetime import datetime
from admin_client.base_Action import BaseAdminAction

class ViewServersAction(BaseAdminAction):
    
    def execute(self):
        print("\nList of external servers:")
        response = self.__safe_execute(self.api_client.make_request, 'GET',
                        'admin/external_servers', current_user=self.get_current_user())
        
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
            print("Failed to retrieve server status.")
            
    
    
    def __print_server_details(self, response):
        for index, server in enumerate(response['servers']):
            status_text = self.__get_server_status(server['status'])
            formatted_date = self.__get_formatted_date(server['last_accessed'])
            print(f"{index+1}. {server['name']} - {status_text} - last accessed: {formatted_date}")
    
    
    def __get_server_status(self, server_status):
        return "Active" if server_status == 'active' else "Not Active"


    def __get_formatted_date(self, raw_date):
        try:
            parsed_date = datetime.strptime(raw_date, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = parsed_date.strftime("%d %b %Y")
        except ValueError:
            formatted_date = "Invalid Date"
        
        return formatted_date
