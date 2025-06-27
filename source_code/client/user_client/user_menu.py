from datetime import datetime, date
from utils import display_articles, get_date
from utils import print_menu, get_valid_article_id
from user_client.handle_menu.headlines import Headlines
class UserMenu:
    def __init__(self, api_client, get_current_user, set_current_user,
                 article_service, notification_service, user_service):
        self.api_client = api_client
        self.get_user = get_current_user
        self.set_user = set_current_user
        self.article_service = article_service
        self.notification_service = notification_service
        self.user_service = user_service

    def run_menu(self):
        response = True
        while True and response:
            self.__welcome_user()
            choice = print_menu("Main Menu", [
                "Headlines", "Saved Articles", "Search", "Notifications", "Logout"
            ])

            if choice == '1':
                response = self.__headlines_menu()
            elif choice == '2':
                self.__saved_articles_menu()
            elif choice == '3':
                self.__search_menu()
            elif choice == '4':
                self.__notifications_menu()
            elif choice == '5':
                self.user_service.logout()
                break
            else:
                print("Invalid option. Try again.")

    def __welcome_user(self):
        user = self.get_user()
        if user and 'username' in user:
            now = datetime.now()
            print(f"\nWelcome {user['username']}! Date: {now.strftime('%d-%b-%Y')} Time: {now.strftime('%I:%M%p')}")
        else:
            print("⚠️ User not logged in.")

    def __headlines_menu(self):
        response = True
        while True and response:
            choice = print_menu("Headlines", ["Today", "Date range", "Back"])
            if choice == '1':
                response = self.__show_headlines("today", str(date.today()), str(date.today()))
            elif choice == '2':
                start, end = get_date()
                response = self.__show_headlines("range", start, end)
            elif choice == '3':
                break
            else:
                print("Invalid option.")
        
        return response


    def __show_headlines(self, timeframe, start_date, end_date):
        categories_resp = self.api_client.make_request('GET', 'user/categories', current_user=self.get_user())
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
            return True

        selected = category_map.get(choice)
        
        params = {'start_date': start_date, 'end_date': end_date}
        if selected:
            params['category'] = selected

        response = self.api_client.make_request('GET', 'user/news', params=params, current_user=self.get_user())
        articles = response.get('articles', []) if response.get('success') else []
        display_articles(articles)

        if articles:
            response = self.__article_interaction_loop()
            return response
        
        return True

    def __article_interaction_loop(self):
        response = True
        while True:
            choice = print_menu("Article Options", ["Back", "Logout", "Save Article", "Like/Dislike Article", "Report Article"])
            if choice == '1':
                break
            elif choice == '2':
                self.user_service.logout()
                return False
            elif choice in ['3', '4']:
                self.__handle_like_dislike(choice)
                
            elif choice in ["5"]:
                self.__handle_report_article()
            else:
                print("Invalid option.")

        return response
    
    def __handle_like_dislike(self, choice):
        article_id = get_valid_article_id()
        if article_id is not None:
            if choice == '3':
                resp = self.article_service.save_article(article_id)
                print(resp.get('message', "Failed to save article."))
            else:
                self.__react_to_article(article_id)
    
    def __handle_report_article(self):
        article_id = get_valid_article_id()
        report_reason  = input("Enter the article report reason\n")
        if article_id is not None:
                resp = self.article_service.report_article(article_id, report_reason)
                print(resp)
        else:
            print("Artical Reporting Failed")


    
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


    def __saved_articles_menu(self):
        print("\n--- Saved Articles ---")
        response = self.article_service.get_saved_articles()
        if isinstance(response, list) and response[0].get('success'):
            display_articles(response[0].get('articles', []))
        else:
            print("Failed to load saved articles.")
            return

        while True:
            choice = print_menu("Manage Saved Articles", ["Back", "Logout", "Delete Article"])
            if choice == '1':
                break
            elif choice == '2':
                self.user_service.logout()
                return
            elif choice == '3':
                article_id = get_valid_article_id()
                if article_id is not None:
                    result = self.article_service.delete_article(article_id)
                    print(result.get('message', "Failed to delete article."))
            else:
                print("Invalid option.")

    def __search_menu(self):
        print("\n--- Search News ---")
        query = input("Enter keyword(s): ").strip()
        if not query:
            print("Search query can't be empty.")
            return

        start, end = get_date()
        params = {
            'q': query, 'limit': 20, 'offset': 0,
            'start_date': start.strftime('%Y-%m-%d'),
            'end_date': end.strftime('%Y-%m-%d')
        }
        response = self.api_client.make_request('GET', 'user/news', params=params, current_user=self.get_user())
        if response.get('success'):
            articles = response.get('articles', [])
            display_articles(articles)
            if articles:
                self.__article_interaction_loop()
            else:
                print("No results found.")
        else:
            print("Search failed.")

    def __notifications_menu(self):
        while True:
            choice = print_menu("Notifications", ["View", "Configure", "Back", "Logout"])
            if choice == '1':
                self.__view_notifications()
            elif choice == '2':
                self.__configure_notifications()
            elif choice == '3':
                return
            elif choice == '4':
                self.user_service.logout()
                return
            else:
                print("Invalid option.")

    def __view_notifications(self):
        response = self.notification_service.get_notifications()
        if response.get('success'):
            notifications = response.get('notifications', [])
            if not notifications:
                print("No notifications found.")
                return
            for i, n in enumerate(notifications, 1):
                print(f"{i}. Category ID: {n.get('category_id')}, Articles: {n.get('article_ids')}")
                print(f"   Message: {n.get('message')}")
                print(f"   Sent At: {n.get('sent_at')}")
                print("-" * 40)
        else:
            print("Failed to load notifications.")

    def __configure_notifications(self):
        while True:
            prefs = self.notification_service.get_user_preferences()
            categories_resp = self.api_client.make_request('GET', 'user/categories', current_user=self.get_user())
            if not (prefs and prefs.get('success') and categories_resp.get('success')):
                print("Failed to load preferences or categories.")
                return

            categories = categories_resp.get("categories", [])
            enabled = {p['name']: p['enabled'] for p in prefs['preferences'].get('category_preferences', [])}

            print("\n--- Notification Categories ---")
            for idx, cat in enumerate(categories, 1):
                status = "Enabled" if enabled.get(cat['name'], False) else "Disabled"
                print(f"{idx}. {cat['name']} - {status}")
            print(f"{len(categories) + 1}. Manage Keywords")
            print(f"{len(categories) + 2}. Back")
            print(f"{len(categories) + 3}. Logout")

            option = input("Choose an option: ").strip()
            try:
                opt = int(option)
                if 1 <= opt <= len(categories):
                    cat_name = categories[opt - 1]['name']
                    resp = self.notification_service.toggle_category_notification(cat_name)
                    print(resp.get('message', "Failed to update setting."))
                elif opt == len(categories) + 1:
                    self.__manage_keywords()
                elif opt == len(categories) + 2:
                    return
                elif opt == len(categories) + 3:
                    self.user_service.logout()
                    return
                else:
                    print("Invalid option.")
            except ValueError:
                print("Invalid input.")

    def __manage_keywords(self):
        prefs = self.notification_service.get_user_preferences()
        keywords = [p['name'] for p in prefs['preferences'].get('category_preferences', [])]

        print(f"\nCurrent Keywords: {', '.join(keywords) or 'None'}")
        choice = print_menu("Manage Keywords", ["Add Keyword(s)", "Remove Keyword", "Back"])
        
        category_name = input("Enter the Category For Keywords:-  ")

        if choice == '1':
            new_keywords = input("Enter comma-separated keywords: ").strip().lower().split(',')
            new_keywords = [k.strip() for k in new_keywords if k.strip()]
            resp = self.notification_service.update_keywords(category_name, new_keywords)
            print(resp.get('message', 'Failed to add keywords.'))

        elif choice == '2':
            if not keywords:
                print("No keywords to remove.")
                return
            print("\nKeywords:")
            for idx, kw in enumerate(keywords, 1):
                print(f"{idx}. {kw}")
            to_remove = input("Enter number of keyword to remove: ").strip()
            try:
                idx = int(to_remove) - 1
                if 0 <= idx < len(keywords):
                    updated = keywords[:idx] + keywords[idx+1:]
                    resp = self.notification_service.update_keywords(category_name, updated)
                    print(resp.get('message', 'Failed to remove keyword.'))
                else:
                    print("Invalid keyword number.")
            except ValueError:
                print("Invalid input.")

        elif choice == '3':
            return

        else:
            print("Invalid option.")
