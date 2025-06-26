from database.database import db
from flask import jsonify 

class ReportArticleRepository:
    
    def get_article_by_id(self, article_id):
        try:
            query = "SELECT * FROM news_articles WHERE id = %s"
            row = db.execute_query(query, (article_id,), fetch_one=True)
            return row
        
        except Exception as error:
            return jsonify(error)
    

    def hide_article(self, article_id):
        try:
            db.execute_query("UPDATE news_articles SET is_hidden = 1 WHERE id = %s", (article_id,))
            return f"Article {article_id} hide successfully.", 200
            
        except Exception as error:
            print(error)
            return f"Article {article_id} Hide Failed", 502
              
            

    def increment_report_count(self, article_id):
        try:
            
            db.execute_query("""
                        UPDATE news_articles
                        SET report_count = report_count + 1
                        WHERE id = %s
                    """, (article_id,))
            return f"Article {article_id} Reported successfully.", 200

        except Exception as error:
            print(error)
            return f"Article {article_id} Report Failed", 502


    def add_report(self, user_id, article_id, reason):
        try:
            db.execute_query("""
                        INSERT INTO article_reports (user_id, article_id, reason)
                        VALUES (%s, %s, %s)
                    """, (user_id, article_id, reason))
            return f"Article {article_id} Report added successfully.", 200

        except Exception as error:
            print(error)
            return f"Article {article_id} report insertion failed.", 502
    
    
    def hide_by_keyword(self, keyword):
        try:
            db.execute_query("""
                        INSERT INTO article_filters (keyword)
                        VALUES (%s)""", (keyword,))
            
            keyword = f"%{keyword}%"
            
            db.execute_query("""
                        UPDATE news_articles AS na
                        JOIN (
                            SELECT id FROM news_articles
                            WHERE (title LIKE %s OR description LIKE %s OR raw_data LIKE %s)
                        ) AS subquery ON na.id = subquery.id
                        SET na.is_hidden = 1""", (keyword, keyword, keyword))

            return f"Article related to {keyword} will be hidden successfully.", 200


        except Exception as error:
            print(error)
            return f"Article related to {keyword} hidden operation failed.", 502
