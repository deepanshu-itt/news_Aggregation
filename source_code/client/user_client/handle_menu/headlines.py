from datetime import datetime, date
from utils import display_articles, get_date
from utils import print_menu, get_valid_article_id

class Headlines:
    def __init__(self, api_client, get_user, set_user,
                 article_service, notification_service, user_service):
        self.api_client = api_client
        self.get_current_user = get_user
        self.set_current_user = set_user
        self.article_service = article_service
        self.notification_service = notification_service
        self.user_service = user_service
        
    def headlines_menu(self):
        while True:
            choice = print_menu("Headlines", ["Today", "Date range", "Back"])
            if choice == '1':
                self.__show_headlines("today", str(date.today()), str(date.today()))
            elif choice == '2':
                start, end = get_date()
                self.__show_headlines("range", start, end)
            elif choice == '3':
                break
            else:
                print("Invalid option.")
    
    
    
    def __show_headlines(self,timeframe, start_date, end_date):
        categories_resp = self.api_client.make_request('GET', 'user/categories', current_user=self.get_current_user())
        categories = categories_resp.get("categories", [])
        category_map = {'1': None}
        print("\n--- Select a Category ---")
        print("1. All")
        for idx, cat in enumerate(categories, start=2):
            print(f"{idx}. {cat['name']}")
            category_map[str(idx)] = cat['name']
        print(f"{len(categories) + 2}. Back")

        choice = input("Select an option: ").strip()
        if choice == str(len(categories) + 2):
            return

        selected = category_map.get(choice)
        params = {'start_date': start_date, 'end_date': end_date}
        if selected:
            params['category'] = selected

        response = self.api_client.make_request('GET', 'user/news', params=params, current_user=self.get_current_user())
        articles = response.get('articles', []) if response.get('success') else []
        display_articles(articles)

        if articles:
            self.__article_interaction_loop()
    

    def __article_interaction_loop(self):
        while True:
            choice = print_menu("Article Options", ["Back", "Logout", "Save Article", "Like/Dislike"])
            if choice == '1':
                break
            elif choice == '2':
                self.user_service.logout()
                return
            elif choice in ['3', '4']:
                self.__handle_like_dislike()
            else:
                print("Invalid option.")
    
    
    @staticmethod
    def __handle_like_dislike(self, choice):
        article_id = get_valid_article_id()
        if article_id is not None:
            if choice == '3':
                resp = self.article_service.save_article(article_id)
                print(resp.get('message', "Failed to save article."))
            else:
                Headlines.__react_to_article(article_id)
    
    
    @staticmethod
    def __react_to_article(self, article_id):
        reaction = input("1. Like\n2. Dislike\nChoose reaction: ").strip()
        if reaction == '1':
            result = self.article_service.react_to_article(article_id, "like")
        elif reaction == '2':
            result = self.article_service.react_to_article(article_id, "dislike")
        else:
            print("Invalid reaction.")
            return
        print(result.get('message', "Failed to react to article."))