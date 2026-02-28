"""
API Routes
"""
from flask import Blueprint, request, jsonify, current_app
from models import db, SearchHistory, SavedRecommendation
from ml.tfidf_model import TFIDFRecommender
from ml.neural_model import NeuralRecommender
from ml.utils import get_courses_data, save_recommendation_history, save_recommendation
import json

api_bp = Blueprint('api', __name__)

# Initialize models
tfidf_model = None
neural_model = None

def get_tfidf_model():
    """Get or initialize TF-IDF model"""
    global tfidf_model
    if tfidf_model is None:
        tfidf_model = TFIDFRecommender(
            current_app.config['TFIDF_VECTORIZER_PATH'],
            current_app.config['TFIDF_MODEL_PATH']
        )
        
        # Try to load existing model
        loaded = tfidf_model.load_model()
        # if loading succeeded but no dataframe present, retrain
        if not loaded or tfidf_model.courses_df is None:
            courses_df = get_courses_data(current_app)
            tfidf_model.train(courses_df)
    
    return tfidf_model

def get_neural_model():
    """Get or initialize Neural model"""
    global neural_model
    if neural_model is None:
        neural_model = NeuralRecommender(
            current_app.config['NEURAL_MODEL_NAME']
        )
        
        # Try to load existing model
        model_path = current_app.config['MODEL_CACHE_DIR'] + '/neural_model.joblib'
        if not neural_model.load_model(model_path):
            # Train new model
            courses_df = get_courses_data(current_app)
            neural_model.train(courses_df)
            neural_model.save_model(model_path)
    
    return neural_model

@api_bp.route('/recommend', methods=['POST'])
def recommend():
    """Get course recommendations"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        model_type = data.get('model', 'tfidf')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Get recommendations based on model type
        if model_type == 'tfidf':
            model = get_tfidf_model()
        elif model_type == 'neural':
            model = get_neural_model()
        else:
            return jsonify({'error': 'Invalid model type'}), 400
        
        recommendations = model.recommend(query, top_n=10)
        
        # Save to search history
        search_id = save_recommendation_history(
            db, SearchHistory, query, model_type, recommendations
        )
        
        return jsonify({
            'success': True,
            'search_id': search_id,
            'query': query,
            'model': model_type,
            'recommendations': recommendations
        })
        
    except Exception as e:
        current_app.logger.exception("Error in /api/recommend")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/history', methods=['GET'])
def get_history():
    """Get search history"""
    try:
        # Get all search history
        history = db.session.query(SearchHistory).order_by(
            SearchHistory.timestamp.desc()
        ).all()
        
        # Group by query to show differences
        query_groups = {}
        for item in history:
            if item.query not in query_groups:
                query_groups[item.query] = []
            query_groups[item.query].append(item.to_dict())
        
        return jsonify({
            'success': True,
            'history': [h.to_dict() for h in history],
            'query_groups': query_groups
        })
        
    except Exception as e:
        current_app.logger.exception("Error in /api/history")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/save', methods=['POST'])
def save_recommendations():
    """Save recommendations"""
    try:
        data = request.get_json()
        search_id = data.get('search_id')
        course_id = data.get('course_id')
        
        if not search_id or not course_id:
            return jsonify({'error': 'search_id and course_id are required'}), 400
        
        # Get the search history
        # use session.get to avoid attribute collision with 'query' column
        search = db.session.get(SearchHistory, search_id)
        if not search:
            return jsonify({'error': 'Search not found'}), 404
        
        # Parse results to find the course
        results = json.loads(search.results)
        course_data = None
        for course in results:
            if course['course_id'] == course_id:
                course_data = course
                break
        
        if not course_data:
            return jsonify({'error': 'Course not found in results'}), 404
        
        # Check if already saved
        existing = SavedRecommendation.query.filter_by(
            search_history_id=search_id,
            course_id=course_id
        ).first()
        
        if existing:
            return jsonify({'error': 'Recommendation already saved'}), 400
        
        # Save recommendation
        save_recommendation(db, SavedRecommendation, search_id, course_id, course_data)
        
        return jsonify({
            'success': True,
            'message': 'Recommendation saved successfully'
        })
        
    except Exception as e:
        current_app.logger.exception("Error in /api/save")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/compare/<query>', methods=['GET'])
def compare_models(query):
    """Compare TF-IDF vs Neural for same query"""
    try:
        # Get TF-IDF recommendations
        tfidf_model = get_tfidf_model()
        tfidf_results = tfidf_model.recommend(query, top_n=10)
        
        # Get Neural recommendations
        neural_model = get_neural_model()
        neural_results = neural_model.recommend(query, top_n=10)
        
        # Analyze differences
        tfidf_courses = {r['course_id']: r for r in tfidf_results}
        neural_courses = {r['course_id']: r for r in neural_results}
        
        common = set(tfidf_courses.keys()) & set(neural_courses.keys())
        tfidf_only = set(tfidf_courses.keys()) - set(neural_courses.keys())
        neural_only = set(neural_courses.keys()) - set(tfidf_courses.keys())
        
        return jsonify({
            'success': True,
            'query': query,
            'tfidf': {
                'results': tfidf_results,
                'count': len(tfidf_results)
            },
            'neural': {
                'results': neural_results,
                'count': len(neural_results)
            },
            'comparison': {
                'common_courses': len(common),
                'tfidf_only': len(tfidf_only),
                'neural_only': len(neural_only)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500