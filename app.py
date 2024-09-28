from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models.user import db
from routes.auth import auth_bp
from routes.books import books_bp
from routes.loans import loans_bp
from utils.logger import logger
import config

app = Flask(__name__)
app.config.from_object(config.Config)
CORS(app)
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()  # Create tables if they don't exist

app.register_blueprint(auth_bp)
app.register_blueprint(books_bp)
app.register_blueprint(loans_bp)

if __name__ == '__main__':
    logger.info("Starting Flask app on port 5000")
    app.run(port=5000)
