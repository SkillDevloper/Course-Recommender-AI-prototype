"""
Application Configuration Settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MODEL_CACHE_DIR = 'ml/models'
    DATA_DIR = 'ml/data'
    TFIDF_MODEL_PATH = f'{MODEL_CACHE_DIR}/tfidf_model.joblib'
    TFIDF_VECTORIZER_PATH = f'{MODEL_CACHE_DIR}/tfidf_vectorizer.joblib'
    NEURAL_MODEL_NAME = 'all-MiniLM-L6-v2'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}