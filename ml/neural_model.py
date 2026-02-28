"""
Neural Model Implementation using Sentence Transformers
"""
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from typing import List, Dict
from .utils import clean_text, normalize_scores
import os

class NeuralRecommender:
    """Neural embedding based course recommender"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.course_embeddings = None
        self.courses_df = None
        
    def train(self, courses_df: pd.DataFrame):
        """Train neural model on course descriptions"""
        self.courses_df = courses_df.copy()
        
        # Clean text
        self.courses_df['clean_description'] = self.courses_df['description'].apply(clean_text)
        
        # Load pre-trained model
        self.model = SentenceTransformer(self.model_name)
        
        # Generate embeddings
        descriptions = self.courses_df['clean_description'].tolist()
        self.course_embeddings = self.model.encode(
            descriptions,
            show_progress_bar=False,
            normalize_embeddings=True
        )
        
    def save_model(self, model_path: str):
        """Save trained model embeddings"""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump({
            'embeddings': self.course_embeddings,
            'courses_df': self.courses_df
        }, model_path)
        
    def load_model(self, model_path: str):
        """Load trained model embeddings"""
        if os.path.exists(model_path):
            data = joblib.load(model_path)
            self.course_embeddings = data['embeddings']
            self.courses_df = data['courses_df']
            self.model = SentenceTransformer(self.model_name)
            return True
        return False
    
    def recommend(self, query: str, top_n: int = 10) -> List[Dict]:
        """Get recommendations for a query"""
        # ensure both model and embeddings are initialized
        if self.model is None or self.course_embeddings is None:
            raise ValueError("Model not trained or loaded")
        
        # Generate query embedding
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )
        
        # Calculate similarity
        similarities = cosine_similarity(query_embedding, self.course_embeddings).flatten()
        
        # Normalize scores
        similarities = normalize_scores(similarities)
        
        # Get top N courses
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        # Prepare results
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:
                course = self.courses_df.iloc[idx]
                results.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'department': course['department'],
                    'description': course['description'],
                    'relevance_score': float(similarities[idx]),
                    'model': 'neural'
                })
        
        return results
    
    def batch_recommend(self, queries: List[str], top_n: int = 10) -> List[List[Dict]]:
        """Get recommendations for multiple queries"""
        return [self.recommend(query, top_n) for query in queries]