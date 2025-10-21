import os

from dotenv import load_dotenv
from flask import Blueprint,Flask, jsonify
from flask_cors import CORS

from extensions import db, ma
from routes.applications import application_bp

load_dotenv()


def create_app(test_config=False):
    app = Flask(__name__)

    # Enabling CORS for frontend-backend communication
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # DB Configuration
    if test_config:
        # In-memory for testing
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        # USE DB URL from env, fallback to local SQLite
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URL", "sqlite:///loan_app.db"
        )

    # Secret key from env, fallback to defaultsecret
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "defaultsecret")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize DB and Marshmallow
    db.init_app(app)
    ma.init_app(app)

     # ========================================
    # Health Check Endpoint
    # ========================================
    
    bp = Blueprint("health", __name__)

    @bp.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200


    # Register Blueprints
    app.register_blueprint(bp, url_prefix="/api")
    app.register_blueprint(application_bp, url_prefix="/api")

   


    return app
