from admin_client.base_Action import BaseAdminAction
from services.external_servers_service import ExternalServersService


class UpdateServerAction(BaseAdminAction):
    def execute(self):
        print("\nUpdate/Edit the external server’s details")
     
        server_id = self.__get_server_id_from_user()
        new_api_key = self.__get_api_key_from_user()
        new_status = self.__get_server_status_from_user()

        payload = self.__create_payload(new_api_key, new_status)

        if not payload:
            print("No changes specified.")
            return

        response = self.__update_server_service(server_id, payload)
    
        self.__is_valid_response(response)
    
    
    def __update_server_service(self, server_id, payload):
        external_server_service = ExternalServersService(self.api_client, self.get_current_user)
        return self.__safe_execute(external_server_service.update_server, server_id, payload)


    def __get_server_id_from_user(self):
        try:
            server_id = int(input("Enter the external server ID: "))
            return server_id
        except ValueError:
            print("Invalid server ID. Please enter a number.")
            return


    def __get_api_key_from_user(self):
        new_api_key = input("Enter the updated API key (leave blank for no change): ").strip()
        return new_api_key
        


    def __get_server_status_from_user(self):
        while True:
            new_status = input("Enter new status (active/inactive, leave blank for no change): ").strip().lower()
            if new_status in ['active', 'inactive']:
                return new_status
            else:
                print("Enter Valid status.")


    def __create_payload(self, new_api_key, new_status):
        payload = {}
        if new_api_key:
            payload['api_key'] = new_api_key
        if new_status in ['active', 'inactive']:
            payload['status'] = new_status
        elif new_status:
            print("Invalid status. Must be 'active' or 'inactive'. Status not changed.")

        return payload


    def __safe_execute(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print("An error occurred while executing the operation.")
            return None

    
    def __is_valid_response(self, response):
        if response and response.get('success'):
            print(response['message'])
        else:
            print("Failed to update server details.")
