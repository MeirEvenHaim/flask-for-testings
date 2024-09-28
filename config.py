import os

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')  # For SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_secret_key')  # Change this to a secure key
    JWT_ACCESS_TOKEN_EXPIRES = 7200  # Token expiration time in seconds (2 hours)
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')  # Allow all origins by default
    CORS_HEADERS = ['Content-Type', 'Authorization']  # Specify allowed headers
    
    # Logging Configuration
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')  # Default logging level
    LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'  # Logging format
    LOGGING_LOCATION = os.environ.get('LOGGING_LOCATION', 'app.log')  # Log file location

    # Additional Configurations (optional)
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'  # Enable debug mode based on environment variable
