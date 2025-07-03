from admin_client.base_Action import BaseAdminAction

class HideArticlesByKeywordsAction(BaseAdminAction):
    def execute(self):
        print("\nHide Articles By Keywords")
        keyword = input("Enter the Keyword: ")
        response = self.__safe_execute(self.api_client.make_request, 'POST', 
                        'admin/hide_article/keywords', {'keyword': keyword}, 
                        current_user=self.get_current_user())

        self.__is_valid_response(response)

    
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
            print("Failed to add keyword.")
