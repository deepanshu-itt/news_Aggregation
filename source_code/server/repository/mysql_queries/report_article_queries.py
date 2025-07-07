get_article_by_id_query = "SELECT * FROM news_articles WHERE id = %s"

get_article_by_user_and_article_id_query = "SELECT * FROM article_reports WHERE user_id = %s and article_id = %s"

hide_article_query = "UPDATE news_articles SET is_hidden = 1 WHERE id = %s"

increment_report_count_query = """
                        UPDATE news_articles
                        SET report_count = report_count + 1
                        WHERE id = %s
                    """

insert_article_report_query = """
                        INSERT INTO article_reports (user_id, article_id, reason)
                        VALUES (%s, %s, %s)
                    """

delete_report_by_user_article_id = """
                        DELETE FROM article_reports WHERE user_id = %s AND article_id = %s
                    """

decrement_report_count_query = """
                        UPDATE news_articles
                        SET report_count = report_count - 1
                        WHERE id = %s
                    """

insert_article_filter_query = """INSERT IGNORE INTO article_filters (keyword) VALUES (%s)"""