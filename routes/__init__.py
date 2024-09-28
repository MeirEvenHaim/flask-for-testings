from flask import Blueprint
from flask_cors import CORS
from .auth import auth_bp
from .books import books_bp
from .loans import loans_bp

bp = Blueprint('api', __name__)
CORS(bp)  # Enable CORS for this blueprint

# Registering the routes
bp.register_blueprint(auth_bp)
bp.register_blueprint(books_bp)
bp.register_blueprint(loans_bp)

