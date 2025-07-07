from datetime import datetime

class SavedArticle:
    def __init__(self, id, user_id, article_id, saved_at=None):
        self.id = id
        self.user_id = user_id
        self.article_id = article_id
        self.saved_at = saved_at or datetime.now()
