from database.database import db
from flask import jsonify
from dto.cursor_dto import CursorDto
from repository.mysql_queries.news_article_queries import hide_article_by_keyword_query
from repository.mysql_queries.report_article_queries import (
    decrement_report_count_query,
    delete_report_by_user_article_id,
    get_article_by_id_query,
    get_article_by_user_and_article_id_query,
    hide_article_query,
    insert_article_report_query,
    insert_article_filter_query,
    increment_report_count_query,
)


class ReportArticleRepository:
    
    def get_article_by_id(self, article_id):
        try:
            query = get_article_by_id_query
            cursor_params = CursorDto(query=query, params=(article_id,), fetch_one=True)
            row = db.execute_query(cursor_params)
            return row
        
        except Exception as error:
            return jsonify(error)
    
    
    def get_article_by_user_id_and_article_id(self, user_id, article_id):
        try:
            query = get_article_by_user_and_article_id_query
            cursor_params = CursorDto(query=query, params=(user_id, article_id), fetch_one=True)
            row = db.execute_query(cursor_params)
            return row
        
        except Exception as error:
            return jsonify(error)
    
    

    def hide_article(self, article_id):
        try:
            result = None
            query = hide_article_query
            
            cursor_params = CursorDto(query=query, params=(article_id,))
            db.execute_query(cursor_params)
            
            result =  f"Article {article_id} hide successfully.", 200
            
        except Exception as error:
            print(error)
            result = f"Article {article_id} Hide Failed", 502
        
        return result
              
            

    def increment_report_count(self, article_id):
        try:
            result = None
            query = increment_report_count_query
            cursor_params = CursorDto(query=query, params=(article_id,))
            db.execute_query(cursor_params)
            result =  f"Article {article_id} Reported successfully.", 200

        except Exception as error:
            print(error)
            result =  f"Article {article_id} Report Failed", 502
        
        return result


    def add_report(self, user_id, article_id, reason):
        result = None
        try:
            query = insert_article_report_query
            cursor_params = CursorDto(query=query, params=(user_id, article_id, reason))
            db.execute_query(cursor_params)
            result = f"Article {article_id} Report added successfully.", 200

        except Exception as error:
            print(error)
            result = f"Article {article_id} report insertion failed.", 502
            
        return result
    
    
    def remove_report(self, user_id, article_id):
        result = None
        try:
            query = delete_report_by_user_article_id
            cursor_params = CursorDto(query=query, params=(user_id, article_id))
            db.execute_query(cursor_params)
            result = f"Article {article_id} Report added successfully.", 200

        except Exception as error:
            print(error)
            result = f"Article {article_id} unreport failed.", 502

        return result
    
    
    def decrement_report_count(self, article_id):
        try:
            result = None
            query = decrement_report_count_query
            cursor_params = CursorDto(query=query, params=(article_id,))
            db.execute_query(cursor_params)
            result =  f"Article {article_id} unreported successfully.", 200

        except Exception as error:
            print(error)
            result =  f"Article {article_id} unreport Failed", 502
        
        return result


    def hide_by_keyword(self, keyword):
        result = None
        try:
            query = insert_article_filter_query
            
            cursor_params = CursorDto(query=query, params=(keyword,))
            db.execute_query(cursor_params)
            
            query = hide_article_by_keyword_query 
                
            keyword = f"%{keyword}%"
            cursor_params.query = query
            cursor_params.params = (keyword, keyword, keyword)
            db.execute_query(cursor_params)

            result = f"Article related to {keyword} will be hidden successfully.", 200


        except Exception as error:
            print(error)
            result = f"Article related to {keyword} hidden operation failed.", 502
        
        return result
