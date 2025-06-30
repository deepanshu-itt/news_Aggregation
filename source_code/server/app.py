import sys
from database.database import db
from scheduler import start_scheduler
from config import Config
import unittest
from app_utils import load_external_server_keys_into_app_config
from routes.admin_routes import admin_bp
from main import create_app

app = create_app()

db_instance = db.get_connection()
if not db_instance:
    print("Could not connect to the database. Please check your MySQL server and credentials.", 
        file=sys.stderr)
    sys.exit(1)

@admin_bp.after_request
def refresh_admin_config(response):
    load_external_server_keys_into_app_config(app.config)
    return response

if __name__ == '__main__':
    tests_passed = unittest.TextTestRunner().run(
        unittest.defaultTestLoader.discover("tests")
    ).wasSuccessful()

    if tests_passed:
    # start_scheduler(app.config)
        app.run(debug=True, host='0.0.0.0', port=5000)
