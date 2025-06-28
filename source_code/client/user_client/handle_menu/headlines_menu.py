from datetime import date
from utils import (print_menu, get_date, display_articles, 
                   get_valid_article_id,display_article_information)
from news_api import NewsAPIClient
from user_client.article_service import ArticleService
import requests


class HeadlinesMenu:
    def __init__(self, user_menu):
        self.api_client: NewsAPIClient = user_menu.api_client
        self.get_user = user_menu.get_user
        self.article_service: ArticleService = user_menu.article_service
        self.user_service = user_menu.user_service
        self.article_service = user_menu.article_service


    def safe_execute(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print("An error occurred while executing the operation.")
            return None

    def run(self):
        while True:
            choice = self.safe_execute(print_menu, "Headlines", ["Today", "Date range", "Back"])
            if choice == '1':
                return self.safe_execute(self._show_headlines, str(date.today()), str(date.today()))
            elif choice == '2':
                start, end = self.safe_execute(get_date)
                return self.safe_execute(self._show_headlines, start, end)
            elif choice == '3':
                return True
            else:
                print("Invalid option.")

    def _show_headlines(self, start_date, end_date):
        categories_resp = self.safe_execute(self.api_client.make_request, 'GET', 'user/categories', current_user=self.get_user())
        categories = categories_resp.get("categories", []) if categories_resp else []
        category_map = {'1': None}

        print("\n--- Select a Category ---")
        print("1. All")
        for index, category in enumerate(categories, start=2):
            print(f"{index}. {category['name']}")
            category_map[str(index)] = category['name']
        print(f"{len(categories) + 2}. Back")

        choice = input("Select an option: ").strip()
        if choice == str(len(categories) + 2):
            return True

        selected = category_map.get(choice)
        params = {'start_date': start_date, 'end_date': end_date}
        if selected:
            params['category'] = selected

        response = self.safe_execute(self.api_client.make_request, 'GET', 'user/news', params=params, current_user=self.get_user())
        articles = response.get('articles', []) if response and response.get('success') else []
        self.safe_execute(display_articles, articles)

        if articles:
            return self.safe_execute(self._article_interaction_loop)
        return True

    def _article_interaction_loop(self):
        while True:
            choice = self.safe_execute(print_menu, "Article Options", [
                "Back", "Logout", "View Article Details", "Save Article", "Like/Dislike Article", "Report Article"
            ])
            if choice == '1':
                break
            elif choice == '2':
                return self.safe_execute(self.user_service.logout)
            elif choice == '3':
                self.safe_execute(self._handle_article_details)
            elif choice in ['4', '5']:
                self.safe_execute(self._handle_like_dislike, choice)
            elif choice == '6':
                self.safe_execute(self._handle_report_article)
            else:
                print("Invalid option.")
        return True

    def _handle_article_details(self):
        article_id = self.safe_execute(lambda: int(input("Enter the Article ID:- ")))
        if not article_id:
            return
        headers = {"Content-Type": "application/json"}
        response = self.safe_execute(
            requests.get,
            "http://localhost:5000/api/user/article",
            headers=headers,
            params={'article_id': article_id}
        )
        if response:
            json_data = self.safe_execute(response.json)
            self.safe_execute(self.__handle_article_details_response, json_data)

    def __handle_article_details_response(self, article_details_response):
        if article_details_response and article_details_response.get("success"):
            self.safe_execute(display_article_information, article_details_response.get("article"))
        else:
            print("No Article Information Available.")

    def _handle_like_dislike(self, choice):
        article_id = self.safe_execute(get_valid_article_id)
        if not article_id:
            return
        if choice == '3':
            response = self.safe_execute(self.article_service.save_article, article_id)
            print(response.get('message', "Failed to save article.") if response else "Failed to save article.")
        else:
            self.safe_execute(self._react_to_article, article_id)

    def _react_to_article(self, article_id):
        reaction = input("1. Like\n2. Dislike\nChoose reaction: ").strip()
        if reaction == '1':
            result = self.safe_execute(self.article_service.react_to_article, article_id, "like")
        elif reaction == '2':
            result = self.safe_execute(self.article_service.react_to_article, article_id, "dislike")
        else:
            print("Invalid reaction.")
            return
        print(result.get('message') if result else "Failed to react to article.")

    def _handle_report_article(self):
        article_id = self.safe_execute(get_valid_article_id)
        if not article_id:
            print("Article reporting failed.")
            return
        reason = input("Enter the article report reason:\n")
        response = self.safe_execute(self.article_service.report_article, article_id, reason)
        print(response.get('message', "Failed to report article.") if response else "Failed to report article.")
