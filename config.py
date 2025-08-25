import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # Neon DB connection
    NEON_DATABASE_URL = os.getenv('NEON_DATABASE_URL')
    if NEON_DATABASE_URL and NEON_DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URI = NEON_DATABASE_URL
    else:
        # Fallback to SQLite if Neon DB URL is not properly configured
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///fastfood.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-here')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Cloudinary configuration
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    
    # File upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Neon Auth configuration (if using Neon's authentication)
    NEON_AUTH_ENABLED = os.getenv('NEON_AUTH_ENABLED', 'false').lower() == 'true'
    NEON_AUTH_URL = os.getenv('NEON_AUTH_URL', 'https://api.neon.tech/auth/v1')
    NEON_API_KEY = os.getenv('NEON_API_KEY')