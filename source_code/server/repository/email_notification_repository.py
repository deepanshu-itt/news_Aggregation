import json
from typing import List, Optional
from interfaces.email_notifications import IEmailNotificationRepository
from models.email_notifications import EmailNotification
from dto.email_dto import EmailNotificationDto
from database.database import MySQLDatabaseConnection,Database 
from config import Config
from dto.cursor_dto import CursorDto

mysql_connection = MySQLDatabaseConnection(Config)
db = Database(mysql_connection)


class EmailNotificationRepository(IEmailNotificationRepository):


    def _map_row_to_notification(self, row) -> EmailNotification:
        article_ids = json.loads(row["article_ids"]) if isinstance(row["article_ids"], str) else row["article_ids"]
        return EmailNotification(
            id=row["id"],
            user_id=row["user_id"],
            article_ids=article_ids,
            message=row["message"],
            sent_at=row["sent_at"],
        )


    def create(self, notification: EmailNotificationDto) -> Optional[EmailNotification]:
        result = None
        query = """
        INSERT INTO email_notifications (user_id, article_ids, message)
        VALUES (%s, %s, %s)
        """
        
        try:
            article_ids_json = json.dumps(notification.article_ids)
            cursor_params = CursorDto(query=query, params=(notification.user_id, 
                                article_ids_json, notification.message),commit=True)
            
            notification_id = db.execute_query(cursor_params)
            notification.id = notification_id
            result =  notification
        except Exception as error:
            print(f"Error creating email notification: {error}")
        
        return result


    def get_by_user(self, user_id: int) -> List[EmailNotification]:
        query = """
        SELECT id, user_id, article_ids, message, sent_at
        FROM email_notifications
        WHERE user_id = %s
        ORDER BY sent_at DESC
        """
        cursor_params = CursorDto(query=query, params=(user_id,),fetch_all=True)
        rows = db.execute_query(cursor_params)
        return [self._map_row_to_notification(row) for row in rows] if rows else []


    def delete(self, notification_id: int) -> bool:
        query = "DELETE FROM email_notifications WHERE id = %s"
        cursor_params = CursorDto(query=query, params=(notification_id,),commit=True)
        result = db.execute_query(cursor_params)
        return result is not None
