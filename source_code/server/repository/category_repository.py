from models.category import Category
from database import database

class CategoryRepository:
    def __init__(self, db: database):
        self._db = db

    def create(self, name: str) -> Category | None:
        query = "INSERT INTO categories (name, is_hidden) VALUES (%s)"
        try:
            category_id = self._db.execute_query(query, (name, False), commit=True)
            if category_id:
                return Category(category_id, name)
        except Exception as e:
            if "Duplicate entry" in str(e):
                print(f"Category '{name}' already exists.")
            else:
                print(f"Error creating category: {e}")
        return None

    def find_by_name(self, name: str) -> Category | None:
        query = "SELECT * FROM categories WHERE name = %s"
        data = self._db.execute_query(query, (name,), fetch_one=True)
        return Category(**data) if data else None

    def find_by_id(self, category_id: int) -> Category | None:
        query = "SELECT * FROM categories WHERE id = %s"
        data = self._db.execute_query(query, (category_id,), fetch_one=True)
        return Category(**data) if data else None

    def get_all(self) -> list[Category]:
        query = "SELECT * FROM categories ORDER BY id"
        data = self._db.execute_query(query, fetch_all=True)
        return [Category(**row) for row in data] if data else []

    def get_category_id(self, name: str) -> int | None:
        query = "SELECT id FROM categories WHERE name = %s"
        data = self._db.execute_query(query, (name,), fetch_one=True)
        return data['id'] if data else None

    
    def hideCategory(self, category_id: int):
        query = "update categories SET is_hidden = 1 WHERE id = %s"
        data = self._db.execute_query(query, (category_id,), fetch_one=True)
        query = "update news_articles set is_hidden =1 where category_id = %s"
        data = self._db.execute_query(query, (category_id,), fetch_one=True)
        return data['id'] if data else None
    
    
    def unhideCategory(self, category_id: int):
        query = "update categories SET is_hidden = 0 WHERE id = %s"
        data = self._db.execute_query(query, (category_id,), fetch_one=True)
        query = "update news_articles set is_hidden =0 where category_id = %s"
        data = self._db.execute_query(query, (category_id,), fetch_one=True)
        return data['id'] if data else None