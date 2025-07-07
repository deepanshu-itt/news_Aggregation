from interfaces.database_connection import IDatabaseConnection
import mysql.connector
from mysql.connector import Error
from dto.cursor_dto import CursorDto


class MySQLDatabaseConnection(IDatabaseConnection):

    def __init__(self, config):
        self._config = config
        self._connection = None
        self._connect()


    def _connect(self):
        try:
            self._connection = mysql.connector.connect(
                host=self._config.MYSQL_HOST,
                user=self._config.MYSQL_USER,
                password=self._config.MYSQL_PASSWORD,
                database=self._config.MYSQL_DB,
                ssl_disabled=True,
                autocommit=True,
                
            )
            
            if self._connection.is_connected():
                print(f"Connected to MySQL database: {self._config.MYSQL_DB}")
        except Error as error:
            print(f"Error connecting to MySQL")
            self._connection = None


    def get_connection(self):
        if self._connection is None or not self._connection.is_connected():
            print("Attempting to reconnect to database...")
            self._connect()
        return self._connection


    def execute_query(self, cursor_params : CursorDto):
        db_connection = self.get_connection()
        result = None
        
        if not db_connection:
            print("Cannot execute query: No active database connection.")
        else :
            result = self.__run_cursor(db_connection, cursor_params)

        return result

    
    def __run_cursor(self, db_connection, cursor_params: CursorDto):
        cursor = db_connection.cursor(dictionary=True, buffered=True)
        result = None
        try: 
            cursor.execute(cursor_params.query, cursor_params.params or ())
            result = self.__manage_cursor_operation(cursor, db_connection, cursor_params)

        except Error as error:
            print(f"Error executing query: {error}")
            db_connection.rollback()
        finally:
            cursor.close()
        
        return result
    
    
    def __manage_cursor_operation(self, cursor, db_connection, cursor_params: CursorDto):
        
        result = None
        
        if cursor_params.commit:
            db_connection.commit()
            result = cursor.lastrowid
        elif cursor_params.fetch_one:
            result = cursor.fetchone()
        elif cursor_params.fetch_all:
            result =  cursor.fetchall()
        
        return result 