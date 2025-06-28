from utils import print_menu
from news_api import NewsAPIClient
from user_client.notification_service import NotificationService

class NotificationsMenu:
    def __init__(self, user_menu):
        self.notification_service: NotificationService = user_menu.notification_service
        self.api_client: NewsAPIClient = user_menu.api_client
        self.get_user = user_menu.get_user
        self.user_service = user_menu.user_service


    def run(self):
        while True:
            choice = print_menu("Notifications", ["View", "Configure", "Back", "Logout"])
            if choice == '1':
                self._view_notifications()
            elif choice == '2':
                return self._configure_notifications()
            elif choice == '3':
                return True
            elif choice == '4':
                self.user_service.logout()
                return False
            else:
                print("Invalid option.")


    def _view_notifications(self):
        response = self.notification_service.get_notifications()
        if not response.get('success'):
            print("Failed to load notifications.")
            return


        notifications = response.get('notifications', [])
        if not notifications:
            print("No notifications found.")
            return


        for index, notification in enumerate(notifications, 1):
            print(f"{index}. Category ID: {notification.get('category_id')}, Articles: {notification.get('article_ids')}")
            print(f"   Message: {notification.get('message')}")
            print(f"   Sent At: {notification.get('sent_at')}")
            print("-" * 40)


    def _configure_notifications(self):
        preferences = self.notification_service.get_user_preferences()
        categories_response = self.api_client.make_request('GET', 'user/categories', current_user=self.get_user())
        if not preferences.get('success') or not categories_response.get('success'):
            print("Failed to load preferences or categories.")
            return True


        categories = categories_response.get("categories", [])
        enabled = {category_preference['name']: category_preference['enabled'] 
                   for category_preference in 
                   preferences['preferences'].get('category_preferences',
                    [])}

        while True:
            self._print_category_settings(categories, enabled)
            option = input("Choose an option: ").strip()
            try:
                option = int(option)
                if 1 <= option <= len(categories):
                    category_name = categories[option - 1]['name']
                    self._toggle_category(category_name)
                elif option == len(categories) + 1:
                    self._manage_keywords(preferences)
                elif option == len(categories) + 2:
                    return True
                elif option == len(categories) + 3:
                    self.user_service.logout()
                    return False
                else:
                    print("Invalid option.")
            except ValueError:
                print("Invalid input.")
        return True


    def _print_category_settings(self, categories, enabled):
        print("\n--- Notification Categories ---")
        for index, category in enumerate(categories, 1):
            category_status = "Enabled" if enabled.get(category['name'], False) else "Disabled"
            print(f"{index}. {category['name']} - {category_status}")
        print(f"{len(categories) + 1}. Manage Keywords")
        print(f"{len(categories) + 2}. Back")
        print(f"{len(categories) + 3}. Logout")


    def _toggle_category(self, category_name):
        response = self.notification_service.toggle_category_notification(category_name)
        print(response.get('message', "Failed to update setting."))


    def _manage_keywords(self, preferences):
        category_preferences = preferences['preferences'].get('category_preferences', [])
        if not category_preferences:
            print("No categories available.")
            return

        self._print_category_list(category_preferences)
        selected = self._select_category(category_preferences)
        if not selected:
            return

        self._category_action(selected)


    def _print_category_list(self, categories):
        print("\nAvailable Categories:")
        for index, category in enumerate(categories, 1):
            print(f"{index}. {category['name']}")


    def _select_category(self, categories):
        try:
            index = int(input("Select a category number: ")) - 1
            return categories[index]
        except (ValueError, IndexError):
            print("Invalid category selection.")
            return None


    def _category_action(self, category):
        self._print_category_details(category)
        choice = print_menu("Manage Keywords", ["Add Keyword(s)", "Remove Keyword(s)", "Disable Category", "Back"])

        if choice == '1':
            self._add_keywords(category)
        elif choice == '2':
            self._remove_keywords(category)
        elif choice == '3':
            self._disable_category(category)
        elif choice == '4':
            return
        else:
            print("Invalid choice.")


    def _print_category_details(self, category):
        print(f"\nSelected Category: {category['name']}")
        print(f"Enabled: {'Yes' if category.get('enabled', True) else 'No'}")
        keywords = category.get('keywords', [])
        print(f"Current Keywords: {', '.join(keywords) if keywords else 'None'}")


    def _add_keywords(self, category):
        keywords = self._get_keywords_input("Enter comma-separated keywords to add: ")
        if not keywords:
            print("No keywords entered.")
            return
        response = self.notification_service.update_keywords(category['name'], keywords)
        print(response.get('message', 'Failed to add keywords.'))


    def _remove_keywords(self, category):
        keywords = category.get('keywords', [])
        if not keywords:
            print("No keywords to remove.")
            return
        self._print_keyword_list(keywords)
        selected = self._get_selected_keywords(keywords)
        if not selected:
            print("No valid keywords selected.")
            return
        response = self.notification_service.delete_keyword(category['name'], selected)
        print(response.get('message', 'Failed to remove keywords.'))


    def _disable_category(self, category):
        confirm = input(f"Disable '{category['name']}' and clear keywords? (y/n): ").strip().lower()
        if confirm == 'y':
            response = self.notification_service.delete_keyword(category['name'], [])
            print(response.get('message', 'Failed to disable category.'))
        else:
            print("Cancelled.")


    def _print_keyword_list(self, keywords):
        print("\nKeywords:")
        for index, keyword in enumerate(keywords, 1):
            print(f"{index}. {keyword}")


    def _get_selected_keywords(self, keywords):
        try:
            indices = input("Enter keyword numbers to remove (comma-separated): ")
            index_list = [int(index.strip()) - 1 for index in indices.split(',')]
            return [keywords[index] for index in index_list if 0 <= index < len(keywords)]
        except (ValueError, IndexError):
            return []


    def _get_keywords_input(self, message):
        user_input_keywords = input(message).strip().lower().split(',')
        return [keyword.strip() for keyword in user_input_keywords if keyword.strip()]
