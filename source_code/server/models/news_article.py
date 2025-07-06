from datetime import datetime


class NewsArticle:
    def __init__(self, title, description, url, image_url, published_at, source, 
                 category_id, id=None, category_name = None, raw_data=None, 
                 created_at=None, like_count = 0 , dislike_count = 0,
                 is_hidden = False, report_count = 0, views = 0):


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
        self.like_count = like_count
        self.dislike_count = dislike_count
        self.is_hidden = is_hidden 
        self.report_count = report_count
        self.views = views
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "image_url": self.image_url,
            "published_at": self.published_at,
            "source": self.source,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "raw_data": self.raw_data,
            "created_at": self.created_at,
            "like_count": self.like_count,
            "dislike_count": self.dislike_count,
            "is_hidden": self.is_hidden,
            "report_count": self.report_count,
            "views": self.views
        }
