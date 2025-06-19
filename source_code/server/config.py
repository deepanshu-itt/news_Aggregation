import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'news_aggregation_key')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'your_mysql_root_password')
    MYSQL_DB = os.getenv('MYSQL_DB', 'news_aggregator_db')
    NEWS_FETCH_INTERVAL_HOURS = int(os.getenv('NEWS_FETCH_INTERVAL_HOURS', 4))
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'


    def __setattr__(self, name, value):
        super().__setattr__(name, value)

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(f"Configuration key '{key}' not found.")

    def __setitem__(self, key, value):
        setattr(self, key, value)
