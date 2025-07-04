from admin_client.base_Action import BaseAdminAction
from services.category_service import CategoryService



class AddCategoryAction(BaseAdminAction):
    def execute(self):
        print("\nAdd new News Category")
        category_name = input("Enter the Category Name: ")
        response = self.__create_category_service(category_name)
        self.__is_valid_response(response)

    
    def __create_category_service(self, category_name):
        category_service = CategoryService(self.api_client, self.get_current_user)
        return self.__safe_execute(category_service.create_category, category_name)


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
