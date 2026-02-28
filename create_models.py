"""
Script to initialize and train ML models
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from ml.tfidf_model import TFIDFRecommender
from ml.neural_model import NeuralRecommender
from ml.utils import get_courses_data

def main():
    """Initialize and train models"""
    print("Initializing Course Recommender AI Models...")
    
    # Create app context
    app = create_app()
    
    with app.app_context():
        # Load course data
        print("Loading course data...")
        courses_df = get_courses_data(app)
        print(f"Loaded {len(courses_df)} courses")
        
        # Train TF-IDF model
        print("\nTraining TF-IDF model...")
        tfidf_model = TFIDFRecommender(
            app.config['TFIDF_VECTORIZER_PATH'],
            app.config['TFIDF_MODEL_PATH']
        )
        tfidf_model.train(courses_df)
        print("TF-IDF model trained and saved")
        
        # Train Neural model
        print("\nTraining Neural model...")
        neural_model = NeuralRecommender(
            app.config['NEURAL_MODEL_NAME']
        )
        neural_model.train(courses_df)
        neural_model.save_model(app.config['MODEL_CACHE_DIR'] + '/neural_model.joblib')
        print("Neural model trained and saved")
        
        # Test models
        print("\nTesting models with sample queries...")
        test_queries = [
            "python data science",
            "machine learning deep learning",
            "web development javascript",
            "data analysis visualization"
        ]
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            
            tfidf_results = tfidf_model.recommend(query, top_n=3)
            print(f"TF-IDF: {[r['title'][:30] + '...' for r in tfidf_results]}")
            
            neural_results = neural_model.recommend(query, top_n=3)
            print(f"Neural: {[r['title'][:30] + '...' for r in neural_results]}")
        
        print("\n✅ Model initialization complete!")

if __name__ == '__main__':
    main()