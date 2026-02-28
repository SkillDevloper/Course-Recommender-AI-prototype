"""
TF-IDF Model Implementation
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from typing import List, Dict, Tuple
from .utils import clean_text, normalize_scores
import os

class TFIDFRecommender:
    """TF-IDF based course recommender"""
    
    def __init__(self, vectorizer_path: str, model_path: str):
        self.vectorizer_path = vectorizer_path
        self.model_path = model_path
        self.vectorizer = None
        self.course_matrix = None
        self.courses_df = None
        
    def train(self, courses_df: pd.DataFrame):
        """Train TF-IDF model on course descriptions"""
        self.courses_df = courses_df.copy()
        
        # Clean text
        self.courses_df['clean_description'] = self.courses_df['description'].apply(clean_text)
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            min_df=2,
            max_df=0.85,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Fit and transform
        self.course_matrix = self.vectorizer.fit_transform(
            self.courses_df['clean_description']
        )
        
        # Save models
        self.save_model()
        
    def save_model(self):
        """Save trained model, vectorizer, and course dataframe"""
        os.makedirs(os.path.dirname(self.vectorizer_path), exist_ok=True)
        # always save vectorizer separately since path may differ
        joblib.dump(self.vectorizer, self.vectorizer_path)
        # bundle matrix and dataframe together for easier loading
        joblib.dump({
            'course_matrix': self.course_matrix,
            'courses_df': self.courses_df
        }, self.model_path)
        
    def load_model(self):
        """Load trained model, vectorizer, and course dataframe"""
        if os.path.exists(self.vectorizer_path) and os.path.exists(self.model_path):
            self.vectorizer = joblib.load(self.vectorizer_path)
            data = joblib.load(self.model_path)
            # compatible with previous format
            if isinstance(data, dict):
                self.course_matrix = data.get('course_matrix')
                self.courses_df = data.get('courses_df')
            else:
                # older versions saved only matrix
                self.course_matrix = data
                self.courses_df = None
            return True
        return False
    
    def recommend(self, query: str, top_n: int = 10) -> List[Dict]:
        """Get recommendations for a query"""
        # avoid ambiguous truth value checks on sparse arrays
        if self.vectorizer is None or self.course_matrix is None:
            raise ValueError("Model not trained or loaded")
        if self.courses_df is None:
            # this should never happen if model was trained/loaded properly
            raise ValueError("Course dataframe missing from model")
        
        # Clean query
        clean_query = clean_text(query)
        
        # Transform query
        query_vector = self.vectorizer.transform([clean_query])
        
        # Calculate similarity
        similarities = cosine_similarity(query_vector, self.course_matrix).flatten()
        
        # Normalize scores
        similarities = normalize_scores(similarities)
        
        # Get top N courses
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        # Prepare results
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only include relevant results
                course = self.courses_df.iloc[idx]
                results.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'department': course['department'],
                    'description': course['description'],
                    'relevance_score': float(similarities[idx]),
                    'model': 'tfidf'
                })
        
        return results
    
    def batch_recommend(self, queries: List[str], top_n: int = 10) -> List[List[Dict]]:
        """Get recommendations for multiple queries"""
        return [self.recommend(query, top_n) for query in queries]