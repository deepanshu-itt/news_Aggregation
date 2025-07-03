from admin_client.base_Action import BaseAdminAction

class AddCategoryAction(BaseAdminAction):
    def execute(self):
        print("\nAdd new News Category")
        category_name = input("Enter the Category Name: ")
        response = self.__safe_execute(self.api_client.make_request, 'POST', 
                        'admin/categories', {'name': category_name}, current_user=self.get_current_user())
        self.__is_valid_response(response)

    
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
            print("Failed to add new category.")
