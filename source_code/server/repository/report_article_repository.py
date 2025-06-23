from database.database import db
from flask import jsonify 

class ReportArticleRepository:
    
    def get_article_by_id(self, article_id):
        try:
            query = "SELECT * FROM news_articles WHERE id = %s"
            row = db.execute_query(query, (article_id,), fetch_one=True)
            return jsonify(row), 200
        
        except Exception as error:
            return jsonify(error), 502
    

    def hide_article(self, article_id):
        try:
            result =  db.execute_query("UPDATE news_articles SET is_hidden = 1 WHERE id = %s", (article_id,))
            return f"Article {article_id} hide successfully.", 200
        except Exception as error:
            return jsonify(error), 502
              
            

    def increment_report_count(self, article_id):
        try:
            result = db.execute_query("""
                        UPDATE news_articles
                        SET report_count = report_count + 1
                        WHERE id = %s
                    """, (article_id,))
            result = self.get_article_by_id(article_id)
            return jsonify(result), 200
        except Exception as error:
            print(error)
            return jsonify(error), 502


    def add_report(self, user_id, article_id, reason):
        try:
            result = db.execute_query("""
                        INSERT INTO article_reports (user_id, article_id, reason)
                        VALUES (%s, %s, %s)
                    """, (user_id, article_id, reason))
            return f"Article {article_id} Report added successfully.", 200
        except Exception as error:
            print(error)
            return jsonify(error), 502
            

