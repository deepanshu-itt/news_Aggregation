from database.database import db
from flask import jsonify
from dto.cursor_dto import CursorDto

class ReportArticleRepository:
    
    def get_article_by_id(self, article_id):
        try:
            query = "SELECT * FROM news_articles WHERE id = %s"
            cursor_params = CursorDto(query=query, params=(article_id,), fetch_one=True)
            row = db.execute_query(cursor_params)
            return row
        
        except Exception as error:
            return jsonify(error)
    

    def hide_article(self, article_id):
        try:
            result = None
            query = "UPDATE news_articles SET is_hidden = 1 WHERE id = %s"
            
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
            query = """
                        UPDATE news_articles
                        SET report_count = report_count + 1
                        WHERE id = %s
                    """
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
            query = """
                        INSERT IGNORE INTO article_reports (user_id, article_id, reason)
                        VALUES (%s, %s, %s)
                    """
            cursor_params = CursorDto(query=query, params=(user_id, article_id, reason))
            db.execute_query(cursor_params)
            result = f"Article {article_id} Report added successfully.", 200

        except Exception as error:
            print(error)
            result = f"Article {article_id} report insertion failed.", 502
            
        return result
    
    
    def hide_by_keyword(self, keyword):
        result = None
        try:
            query = """INSERT IGNORE INTO article_filters (keyword) VALUES (%s)"""
            
            cursor_params = CursorDto(query=query, params=(keyword,))
            db.execute_query(cursor_params)
            
            query = """
                        UPDATE news_articles AS na
                        JOIN (
                            SELECT id FROM news_articles
                            WHERE (title LIKE %s OR description LIKE %s OR raw_data LIKE %s)
                        ) AS subquery ON na.id = subquery.id
                        SET na.is_hidden = 1"""
                
            keyword = f"%{keyword}%"
            cursor_params.query = query
            cursor_params.params = (keyword, keyword, keyword)
            db.execute_query(cursor_params)

            result = f"Article related to {keyword} will be hidden successfully.", 200


        except Exception as error:
            print(error)
            result = f"Article related to {keyword} hidden operation failed.", 502
        
        return result
