from typing import List
from repository.category_repository import CategoryRepository
from models.user_notification import UserNotification


class ArticleFilter:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def filter_articles(self, user_prefs: UserNotification, articles: List) -> List:
        category_preferences = user_prefs.category_preferences or []
        filtered_articles = []

        for article in articles:
            for cat_pref in category_preferences:
                cat_id = self.category_repo.get_category_id(cat_pref['name'])
                if not cat_id or article.category_id != cat_id:
                    continue
                
                keywords = cat_pref.get('keywords', [])
                article_text = f"{article.title} {article.description or ''}".lower()

                if keywords:
                    if any(keyword.lower() in article_text for keyword in keywords):
                        filtered_articles.append(article)
                        break
                else:
                    filtered_articles.append(article)
                    break

        return filtered_articles
