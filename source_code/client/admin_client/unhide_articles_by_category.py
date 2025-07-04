from admin_client.base_Action import BaseAdminAction

class UnhideArticlesByCategoryAction(BaseAdminAction):
    def execute(self):
        print("\nUnhide Articles By Category")
        category_name = self.__get_already_block_categories()
        unhide_article_api_response = self.__safe_execute(self.api_client.make_request,
                        'POST', 'admin/unhide_category_article', {'name': category_name}, current_user=self.get_current_user())

        self.__is_valid_response(unhide_article_api_response)
    
    
    def __get_already_block_categories(self):
        print("\nAvailable Categories to Unblock\n")
        categories_response = self.__safe_execute(self.api_client.make_request,
                        'GET', 'user/categories', current_user=self.get_current_user())

        categories = categories_response.get("categories", []) if categories_response else []
        category_map = {}
        self.__print_categories(categories, category_map)
        selected_category =  self.__get_user_input_category(category_map)
        print(selected_category)
        return selected_category


    def __print_categories(self, categories, category_map):
        for index, category in enumerate(categories, start=1):
            if (category['is_hidden'] == 1):
                print(f"{index}. {category['name']}")
                category_map[str(index)] = category['name']
       
        
    def __get_user_input_category(self, category_map):
        
        while True:
            user_input_choice = input("Select an option: ").strip()
            if category_map.get(user_input_choice):
                return category_map.get(user_input_choice)
            else:
                print("Enter valid option\n")

    
    def __safe_execute(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print("An error occurred while executing the operation.")
            return None


    def __is_valid_response(self, unhide_article_api_response):
        if unhide_article_api_response and unhide_article_api_response.get('success'):
            print(unhide_article_api_response['message'])
        else:
            print("Failed to unhide articles by category.")
