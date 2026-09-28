from flask import Flask, jsonify
from flask_cors import CORS
from config import config_dict
from app.database import init_db, close_db
from app.routes import pages_bp, api_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    
    app.config.from_object(config_dict[config_name])

    CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*')}})

    init_db(app)

    app.teardown_appcontext(close_db)

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/health')
    def health():
        return jsonify({"status": "active", "message": "SmartLead AI servisi calisiyor."}), 200

    return app