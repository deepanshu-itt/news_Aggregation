from datetime import datetime


class NewsArticleDto:
    def __init__(self, title, description, url, image_url, published_at, source, 
                 category_id, category_name = None, raw_data=None, created_at=None, 
                 is_hidden = False, report_count = 0):
        
        self.id = id
        self.title = title
        self.description = description
        self.url = url
        self.image_url = image_url
        self.published_at = published_at
        self.source = source
        self.category_id = category_id
        self.category_name = category_name
        self.raw_data = raw_data
        self.created_at = created_at if created_at else datetime.now()
        self.is_hidden = is_hidden
        self.report_count = report_count
