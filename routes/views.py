"""
Main View Routes
"""
from flask import Blueprint, render_template, current_app
from models import db, SearchHistory, SavedRecommendation

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Home page"""
    return render_template('home.html')

@main_bp.route('/recommend')
def recommend_page():
    """Recommendation page"""
    return render_template('recommend.html')

@main_bp.route('/dashboard')
def dashboard():
    """User dashboard"""
    # Get search history using session query (column named 'query' conflicts)
    search_history = db.session.query(SearchHistory).order_by(
        SearchHistory.timestamp.desc()
    ).limit(20).all()
    
    # Get saved recommendations grouped by search
    saved_recommendations = {}
    searches_with_saves = db.session.query(SearchHistory).join(
        SavedRecommendation
    ).distinct().order_by(
        SearchHistory.timestamp.desc()
    ).all()
    
    for search in searches_with_saves:
        saves = SavedRecommendation.query.filter_by(
            search_history_id=search.id
        ).all()
        if saves:
            saved_recommendations[search.id] = {
                'search': search.to_dict(),
                'recommendations': [s.to_dict() for s in saves]
            }
    
    return render_template('dashboard.html',
                         search_history=search_history,
                         saved_recommendations=saved_recommendations)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')