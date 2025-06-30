from models.category import Category
from database import database
from dto.cursor_dto import CursorDto
from repository.mysql_queries.category_queries import (
    create_category_query,
    find_by_id_query,
    find_by_name_query,
    get_all_categories_query,
    get_category_id_query,
    hide_category_query,
    unhide_category_query
)


class CategoryRepository:
    def __init__(self, db: database):
        self._db = db

    def create(self, name: str) -> Category | None:
        query = create_category_query
        cursor_params = CursorDto(query=query, params=(name, False), commit=True)
        try:
            category_id = self._db.execute_query(cursor_params)
            if category_id:
                return Category(category_id, name)
        except Exception as error:
            if "Duplicate entry" in str(error):
                print(f"Category '{name}' already exists.")
            else:
                print(f"Error creating category: {error}")
        return None


    def find_by_name(self, name: str) -> Category | None:
        query = find_by_name_query 
        cursor_params = CursorDto(query=query, params=(name,),  fetch_one=True)
        data = self._db.execute_query(cursor_params)
        return Category(**data) if data else None


    def find_by_id(self, category_id: int) -> Category | None:
        query = find_by_id_query
        cursor_params = CursorDto(query=query, params=(category_id,),  fetch_one=True)
        data = self._db.execute_query(cursor_params)
        return Category(**data) if data else None


    def get_all(self) -> list[Category]:
        query = get_all_categories_query
        cursor_params = CursorDto(query=query, fetch_all=True)
        data = self._db.execute_query(cursor_params)
        return [Category(**row) for row in data] if data else []


    def get_category_id(self, name: str) -> int | None:
        query = get_category_id_query
        cursor_params = CursorDto(query=query, params=(name,),  fetch_one=True)
        data = self._db.execute_query(cursor_params)
        return data['id'] if data else None

    
    def hideCategory(self, category_id: int):
        query = hide_category_query
        cursor_params = CursorDto(query=query, params=(category_id,),  fetch_one=True)
        data = self._db.execute_query(cursor_params)
        query = "update news_articles set is_hidden =1 where category_id = %s"
        cursor_params = CursorDto(query=query, params=(category_id,),  fetch_one=True)
        data = self._db.execute_query(cursor_params)
        return data['id'] if data else None
    
    
    def unhideCategory(self, category_id: int):
        query = unhide_category_query
        cursor_params = CursorDto(query=query, params=(category_id,),  fetch_one=True)
        data = self._db.execute_query(cursor_params)
        query = "update news_articles set is_hidden =0 where category_id = %s"
        cursor_params = CursorDto(query=query, params=(category_id,),  fetch_one=True)
        data = self._db.execute_query(cursor_params)
        return data['id'] if data else None
