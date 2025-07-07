create_email_notification_query = """
        INSERT INTO email_notifications (user_id, article_ids, message)
        VALUES (%s, %s, %s)
        """

get_notification_by_user_query = """
        SELECT id, user_id, article_ids, message, sent_at
        FROM email_notifications
        WHERE user_id = %s
        ORDER BY sent_at DESC
        """


delete_notification_by_user_query = "DELETE FROM email_notifications WHERE id = %s"