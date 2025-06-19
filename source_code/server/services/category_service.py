from repository.category_repository import CategoryRepository
from database.database import db
class CategoryService:
    _instance = None
    _category_keywords = {} 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CategoryService, cls).__new__(cls)
            cls._instance._load_category_keywords()
        return cls._instance

    def _load_category_keywords(self):
        self._category_keywords = {
            "business": ["economy", "market", "stocks", "finance", "company", "trade", "ceo", "startup", "investment"],
            "entertainment": ["movie", "film", "music", "celebrity", "hollywood", "tv", "show", "artist", "culture"],
            "sports": ["sport", "team", "game", "match", "league", "athlete", "championship", "football", "basketball", "tennis"],
            "technology": ["tech", "software", "ai", "artificial intelligence", "robotics", "gadget", "internet", "cyber", "innovation", "startup"],
        }
    
    
    @staticmethod
    def getCategories():
        category_repository = CategoryRepository(db = db)
        all_db_categories = {single_category.name.lower(): single_category.id for single_category in category_repository.get_all()}
        return all_db_categories
    
    
    @staticmethod
    def createCategory(name:str):
        category_repository = CategoryRepository(db = db)
        response = category_repository.create(name)
        return response


    def identify_category_from_text(self, title ="event", description="great"):
        category_repository = CategoryRepository(db = db)
        text = ((title or "") + " " + (description or "")).lower()

        all_db_categories = {c.name.lower(): c.id for c in category_repository.get_all()}
        
        for cat_name_lower, cat_id in all_db_categories.items():
            if cat_name_lower in text:
                return cat_id


        for category, keywords in self._category_keywords.items():
            if any(keyword in text for keyword in keywords):
                if category in all_db_categories:
                    return all_db_categories[category]
        
        
        return all_db_categories.get('general')
