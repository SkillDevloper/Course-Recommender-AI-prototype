"""
Database Models
"""
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class SearchHistory(db.Model):
    """Search history model"""
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.Text, nullable=False)
    model_type = db.Column(db.String(20), nullable=False)
    results = db.Column(db.Text)  # JSON string of results
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationship to saved recommendations
    saved_recommendations = db.relationship('SavedRecommendation', 
                                           backref='search', 
                                           lazy=True,
                                           cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'query': self.query,
            'model_type': self.model_type,
            'results': json.loads(self.results) if self.results else [],
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class SavedRecommendation(db.Model):
    """Saved recommendations model"""
    __tablename__ = 'saved_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    search_history_id = db.Column(db.Integer, 
                                 db.ForeignKey('search_history.id'), 
                                 nullable=False)
    course_id = db.Column(db.String(50), nullable=False)
    course_title = db.Column(db.String(200), nullable=False)
    course_department = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.Text, nullable=False)
    relevance_score = db.Column(db.Float, nullable=False)
    saved_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'search_history_id': self.search_history_id,
            'course_id': self.course_id,
            'course_title': self.course_title,
            'course_department': self.course_department,
            'course_description': self.course_description,
            'relevance_score': self.relevance_score,
            'saved_at': self.saved_at.isoformat() if self.saved_at else None
        }