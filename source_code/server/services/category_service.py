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


    def identify_category_from_text(self, title, description):
        result = None
        category_repository = CategoryRepository(db = db)
        text = ((title or "") + " " + (description or "")).lower()

        all_database_categories = {category.name.lower(): category.id for category in category_repository.get_all()}
        
        result = self.identify_category_from_db_categories(text, all_database_categories)
        
        if result is None:
            result = self.identify_category_keywords(text, all_database_categories)
        
        elif result is None:
            result = all_database_categories('general')
        
        return  result
    
    
    def identify_category_from_db_categories(self, text, all_database_categories):
        result = None
        for category_name_lower, category_id in all_database_categories.items():
            if category_name_lower in text:
                result = category_id
        
        return result
    
    
    def identify_category_keywords(self, text, all_database_categories):
        result = None
        for category, keywords in self._category_keywords.items():
            if any(keyword in text for keyword in keywords):
                if category in all_database_categories:
                    return all_database_categories[category]
        
        return result
