from admin_client.base_admin_action import IAdminAction
from services.article_service import ArticleService


class HideArticlesByKeywordsAction(IAdminAction):
    def execute(self):
        print("\nHide Articles By Keywords")
        keyword = input("Enter the Keyword: ")
        response = self.__hide_articles_by_keyword(keyword)

        self.__is_valid_response(response)

    
    def __hide_articles_by_keyword(self, keyword):
        article_service = ArticleService(self.api_client, self.get_current_user)
        return self.__safe_execute(article_service.hide_articles_by_keyword, keyword)
        
        
    
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
