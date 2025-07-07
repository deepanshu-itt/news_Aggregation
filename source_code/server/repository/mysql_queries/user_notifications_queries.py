get_user_notification_by_id_query = "SELECT * FROM user_notifications WHERE user_id = %s"

update_user_notifications_query = """
                UPDATE user_notifications
                SET category_preferences = %s
                WHERE user_id = %s
            """

create_user_notification_query = """
                INSERT INTO user_notifications (user_id, category_preferences, email)
                VALUES (%s, %s, %s)
            """

get_all_users_for_email = """
            SELECT un.*, u.email 
            FROM user_notifications un 
            JOIN users u ON un.user_id = u.id 
        """