import sys
from database.database import db
from scheduler import start_scheduler
from config import Config
import unittest
from app_utils import load_external_server_keys_into_app_config

from main import create_app

app = create_app()

db_instance = db.get_connection()
if not db_instance:
    print("FATAL: Could not connect to the database. Please check your MySQL server and credentials in .env file.", file=sys.stderr)
    sys.exit(1)



if __name__ == '__main__':
    # tests_passed = unittest.TextTestRunner().run(
    #     unittest.defaultTestLoader.discover("tests")
    # ).wasSuccessful()

    # if tests_passed:
    # start_scheduler(app.config)
    app.run(debug=True, host='0.0.0.0', port=5000)
