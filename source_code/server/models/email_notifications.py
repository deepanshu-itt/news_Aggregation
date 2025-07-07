from datetime import datetime
from typing import List, Optional

class EmailNotification:
    def __init__(self, id: int, user_id: int, article_ids: List[int], message: str,
                 sent_at: Optional[datetime] = None):
        self.id = id
        self.user_id = user_id
        self.article_ids = article_ids
        self.message = message
        self.sent_at = sent_at or datetime.now()
