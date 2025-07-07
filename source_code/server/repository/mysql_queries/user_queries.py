create_user_query = "INSERT IGNORE INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)"

get_user_by_id_query =  "SELECT * FROM users WHERE id = %s"

get_user_by_username = "SELECT * FROM users WHERE username = %s"

get_user_by_email = "SELECT * FROM users WHERE email = %s"

update_user_preferences_by_id_query = "UPDATE user_notifications SET category_preferences = %s WHERE user_id = %s"

get_user_preferences_by_id_query = "SELECT category_preferences FROM user_notifications WHERE user_id = %s"