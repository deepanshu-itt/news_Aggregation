from routes.admin.admin_routes import admin_bp
from routes.user.user_routes import user_bp
from routes.user.user_like_routes import article_reaction_bp
from routes.user.report_article_routes import report_article_bp
from routes.user.save_articles_routes import save_article_bp
from routes.user.user_preferences_routes import user_preferences_bp
from routes.auth_routes import auth_bp
from config import Config
import sys
from flask import Flask, jsonify, session


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    if not app.config.get('SECRET_KEY'):
        print("FATAL: SECRET_KEY is not set in .env or config.py. Please generate one and set it.", 
            file=sys.stderr)
        sys.exit(1)


    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(article_reaction_bp, url_prefix='/api/user')
    app.register_blueprint(report_article_bp, url_prefix='/api/user')
    app.register_blueprint(save_article_bp, url_prefix='/api/user')
    app.register_blueprint(user_preferences_bp, url_prefix='/api/user')


    @app.route('/')
    def home():
        return jsonify({"message": "News Aggregation Server is running! Access API at /api"}), 200


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found", 
                    "message": "The requested URL was not found on the server."}), 404


    @app.errorhandler(500)
    def internal_server_error(error):
        print(f"Internal Server Error: {error}", file=sys.stderr)
        return jsonify({"error": "Internal server error", 
                    "message": "Something went wrong on the server."}), 500


    @app.context_processor
    def inject_user():
        user_id = session.get('user_id')
        username = session.get('username')
        role = session.get('role')
        return dict(current_user_id=user_id, current_username=username, current_user_role=role)

    return app
