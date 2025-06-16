import sys
from flask import Flask, jsonify, session
from database.database import db

app = Flask(__name__)

db_instance = db.get_connection()
if not db_instance:
    print("FATAL: Could not connect to the database. Please check your MySQL server and credentials in .env file.", file=sys.stderr)
    sys.exit(1)


if not app.config.get('SECRET_KEY'):
    print("FATAL: SECRET_KEY is not set in .env or config.py. Please generate one and set it.", file=sys.stderr)
    sys.exit(1)


@app.route('/')
def home():
    return jsonify({"message": "News Aggregation Server is running! Access API at /api"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "message": "The requested URL was not found on the server."}), 404

@app.errorhandler(500)
def internal_server_error(error):
    print(f"Internal Server Error: {error}", file=sys.stderr)
    return jsonify({"error": "Internal server error", "message": "Something went wrong on the server."}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)