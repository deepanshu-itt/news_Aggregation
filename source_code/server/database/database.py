import mysql.connector
from mysql.connector import Error
from abc import ABC, abstractmethod
from config import Config


class IDatabaseConnection(ABC):
    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False, commit=False):
        pass


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
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self._connection = None

    def get_connection(self):
        if self._connection is None or not self._connection.is_connected():
            print("Attempting to reconnect to database...")
            self._connect()
        return self._connection

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False, commit=False):
        conn = self.get_connection()
        if not conn:
            print("Cannot execute query: No active database connection.")
            return None

        cursor = conn.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(query, params or ())
            if commit:
                conn.commit()
                return cursor.lastrowid
            elif fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            return None
        except Error as error:
            print(f"Error executing query: {error}")
            conn.rollback()
            return None
        finally:
            cursor.close()


class Database:
    _instance = None

    def __new__(cls, db_connection: IDatabaseConnection):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._db_connection = db_connection
        return cls._instance

    def execute_query(self, *args, **kwargs):
        return self._db_connection.execute_query(*args, **kwargs)

    def get_connection(self):
        return self._db_connection.get_connection()


# Usage
mysql_connection = MySQLDatabaseConnection(Config)
db = Database(mysql_connection)
