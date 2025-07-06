from news_api import NewsAPIClient
from dto.news_api_dto import NewsApiDto

class NotificationService:
    def __init__(self, api_client: NewsAPIClient, get_user):
        self.api_client = api_client
        self.get_user = get_user


    def get_notifications(self):
        get_notification_dto = NewsApiDto(
            method='GET',
            endpoint='user/notifications',
            current_user=self.get_user()
        )

        return self.api_client.make_request(get_notification_dto)


    def update_keywords(self, category_name, keywords):
        update_keywords_dto = NewsApiDto(
            method='PUT',
            endpoint='user/notifications',
            data = {'keywords': keywords, 'category_name': category_name },
            current_user=self.get_user()
        )
        return self.api_client.make_request(update_keywords_dto)


    def delete_keyword(self, category_name, keyword):
        delete_keywords_dto = NewsApiDto(
            method='DELETE',
            endpoint='user/notifications',
            data = {'keywords': keyword, 'category_name': category_name},
            current_user=self.get_user()
        )
        return self.api_client.make_request(delete_keywords_dto)


    def get_user_preferences(self):
        get_user_preferences_dto = NewsApiDto(
            method='GET',
            endpoint='user/userpreferences',
            current_user=self.get_user()
        )
        return self.api_client.make_request(get_user_preferences_dto)


    def toggle_category_notification(self, category_name):
        toggle_category_notification_dto = NewsApiDto(
            method='PUT',
            endpoint='user/notifications',
            data={'keywords': [], 'category_name': category_name },
            current_user=self.get_user()
        )
        return self.api_client.make_request(toggle_category_notification_dto)
