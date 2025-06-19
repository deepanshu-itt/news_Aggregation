import sys
from database.database import db
from main import create_app
from scheduler import start_scheduler

app = create_app()

db_instance = db.get_connection()
if not db_instance:
    print("FATAL: Could not connect to the database. Please check your MySQL server and credentials in .env file.", file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    
    start_scheduler(app.config)
    app.run(debug=True, host='0.0.0.0', port=5000)