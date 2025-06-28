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

        for i, n in enumerate(notifications, 1):
            print(f"{i}. Category ID: {n.get('category_id')}, Articles: {n.get('article_ids')}")
            print(f"   Message: {n.get('message')}")
            print(f"   Sent At: {n.get('sent_at')}")
            print("-" * 40)

    def _configure_notifications(self):
        prefs = self.notification_service.get_user_preferences()
        categories_resp = self.api_client.make_request('GET', 'user/categories', current_user=self.get_user())
        if not prefs.get('success') or not categories_resp.get('success'):
            print("Failed to load preferences or categories.")
            return True

        categories = categories_resp.get("categories", [])
        enabled = {p['name']: p['enabled'] for p in prefs['preferences'].get('category_preferences', [])}

        while True:
            self._print_category_settings(categories, enabled)
            option = input("Choose an option: ").strip()
            try:
                opt = int(option)
                if 1 <= opt <= len(categories):
                    cat_name = categories[opt - 1]['name']
                    self._toggle_category(cat_name)
                elif opt == len(categories) + 1:
                    self._manage_keywords(prefs)
                elif opt == len(categories) + 2:
                    return True
                elif opt == len(categories) + 3:
                    self.user_service.logout()
                    return False
                else:
                    print("Invalid option.")
            except ValueError:
                print("Invalid input.")
        return True

    def _print_category_settings(self, categories, enabled):
        print("\n--- Notification Categories ---")
        for idx, cat in enumerate(categories, 1):
            status = "Enabled" if enabled.get(cat['name'], False) else "Disabled"
            print(f"{idx}. {cat['name']} - {status}")
        print(f"{len(categories) + 1}. Manage Keywords")
        print(f"{len(categories) + 2}. Back")
        print(f"{len(categories) + 3}. Logout")

    def _toggle_category(self, cat_name):
        resp = self.notification_service.toggle_category_notification(cat_name)
        print(resp.get('message', "Failed to update setting."))

    def _manage_keywords(self, prefs):
        category_prefs = prefs['preferences'].get('category_preferences', [])
        if not category_prefs:
            print("No categories available.")
            return

        self._print_category_list(category_prefs)
        selected = self._select_category(category_prefs)
        if not selected:
            return

        self._category_action(selected)

    def _print_category_list(self, categories):
        print("\nAvailable Categories:")
        for idx, cat in enumerate(categories, 1):
            print(f"{idx}. {cat['name']}")

    def _select_category(self, categories):
        try:
            idx = int(input("Select a category number: ")) - 1
            return categories[idx]
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
        resp = self.notification_service.update_keywords(category['name'], keywords)
        print(resp.get('message', 'Failed to add keywords.'))

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
        resp = self.notification_service.delete_keyword(category['name'], selected)
        print(resp.get('message', 'Failed to remove keywords.'))

    def _disable_category(self, category):
        confirm = input(f"Disable '{category['name']}' and clear keywords? (y/n): ").strip().lower()
        if confirm == 'y':
            resp = self.notification_service.delete_keyword(category['name'], [])
            print(resp.get('message', 'Failed to disable category.'))
        else:
            print("Cancelled.")

    def _print_keyword_list(self, keywords):
        print("\nKeywords:")
        for idx, kw in enumerate(keywords, 1):
            print(f"{idx}. {kw}")

    def _get_selected_keywords(self, keywords):
        try:
            indices = input("Enter keyword numbers to remove (comma-separated): ")
            idx_list = [int(i.strip()) - 1 for i in indices.split(',')]
            return [keywords[i] for i in idx_list if 0 <= i < len(keywords)]
        except (ValueError, IndexError):
            return []

    def _get_keywords_input(self, prompt_msg):
        raw = input(prompt_msg).strip().lower().split(',')
        return [k.strip() for k in raw if k.strip()]
