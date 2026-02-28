"""
Main Flask Application Entry Point
"""
import os
from flask import Flask
from config import config
from models import db  # ✅ Import from models.py
import json

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    # custom Jinja filters
    app.jinja_env.filters['fromjson'] = lambda v: json.loads(v)
    
    # Ensure directories exist
    os.makedirs(app.config['MODEL_CACHE_DIR'], exist_ok=True)
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    
    # Register blueprints
    from routes.views import main_bp
    from routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Import models here to avoid circular imports
    from models import SearchHistory, SavedRecommendation
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize sample data if needed
        from ml.utils import load_sample_data
        if not os.path.exists(os.path.join(app.config['DATA_DIR'], 'courses.csv')):
            load_sample_data(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])