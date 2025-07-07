create_saved_article_query = "INSERT IGNORE INTO saved_articles (user_id, article_id) VALUES (%s, %s)"

delete_saved_article_by_user_article_id_query = "DELETE FROM saved_articles WHERE user_id = %s AND article_id = %s"

check_article_saved_query = "SELECT 1 FROM saved_articles WHERE user_id = %s AND article_id = %s"

get_saved_article_by_user_query = "SELECT article_id FROM saved_articles WHERE user_id = %s"