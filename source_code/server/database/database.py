from config import Config
from interfaces.database_connection import IDatabaseConnection
from database.mysql_databse_connection import MySQLDatabaseConnection
from dto.cursor_dto import CursorDto


class Database:
    _instance = None

    def __new__(cls, db_connection: IDatabaseConnection):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._db_connection = db_connection
        return cls._instance

    def execute_query(self, cursor_params: CursorDto, **kwargs):
        return self._db_connection.execute_query(cursor_params)

    def get_connection(self):
        return self._db_connection.get_connection()



mysql_connection = MySQLDatabaseConnection(Config)
db = Database(mysql_connection)
