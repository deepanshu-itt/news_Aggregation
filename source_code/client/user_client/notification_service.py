from news_api import NewsAPIClient


class NotificationService:
    def __init__(self, api_client: NewsAPIClient, get_user):
        self.api_client = api_client
        self.get_user = get_user

    def get_notifications(self):
        return self.api_client.make_request('GET', 'user/notifications', current_user=self.get_user())

    def update_keywords(self, category_name, keywords):
        return self.api_client.make_request('PUT', 'user/notifications',
                {'keywords': keywords, 'category_name': category_name }, current_user=self.get_user())

    def delete_keyword(self, category_name, keyword):
        return self.api_client.make_request('DELETE', 'user/notifications',
                {'keywords': keyword, 'category_name': category_name}, current_user=self.get_user())

    def get_user_preferences(self):
        return self.api_client.make_request('GET', 'user/userpreferences', current_user=self.get_user())

    def toggle_category_notification(self, category_name):
        return self.api_client.make_request('PUT', 'user/notifications',
                {'keywords': [], 'category_name': category_name }, current_user=self.get_user())
