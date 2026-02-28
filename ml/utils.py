"""
Utility functions for ML models and data processing
"""
import pandas as pd
import numpy as np
import joblib
import re
from typing import List, Tuple, Dict
import json
import os

def clean_text(text: str) -> str:
    """Clean and preprocess text"""
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def normalize_scores(scores: np.ndarray) -> np.ndarray:
    """Normalize similarity scores to 0-100%"""
    if len(scores) == 0:
        return scores
    
    # Convert to percentage (0-100)
    scores = scores * 100
    
    # Ensure values are within 0-100 range
    scores = np.clip(scores, 0, 100)
    
    return scores

def create_sample_courses() -> pd.DataFrame:
    """Create sample course dataset"""
    courses = [
        {
            'course_id': 'CS101',
            'title': 'Introduction to Python Programming',
            'department': 'Computer Science',
            'description': 'Learn Python basics, data structures, and control flow for beginners.',
            'keywords': 'python, programming, beginner, basics, data structures'
        },
        {
            'course_id': 'CS201',
            'title': 'Advanced Python for Data Science',
            'department': 'Computer Science',
            'description': 'Python libraries for data analysis: NumPy, Pandas, and data visualization.',
            'keywords': 'python, data science, numpy, pandas, matplotlib, data analysis'
        },
        {
            'course_id': 'CS301',
            'title': 'Machine Learning Fundamentals',
            'department': 'Computer Science',
            'description': 'Supervised and unsupervised learning algorithms with Python implementations.',
            'keywords': 'machine learning, algorithms, scikit-learn, ai, data science'
        },
        {
            'course_id': 'CS302',
            'title': 'Deep Learning with TensorFlow',
            'department': 'Computer Science',
            'description': 'Neural networks, CNN, RNN, and TensorFlow/Keras for deep learning projects.',
            'keywords': 'deep learning, neural networks, tensorflow, keras, cnn, rnn'
        },
        {
            'course_id': 'DS101',
            'title': 'Data Analysis with SQL',
            'department': 'Data Science',
            'description': 'SQL queries, database design, and data extraction techniques.',
            'keywords': 'sql, database, data analysis, queries, data extraction'
        },
        {
            'course_id': 'DS201',
            'title': 'Data Visualization with Tableau',
            'department': 'Data Science',
            'description': 'Create interactive dashboards and visualizations using Tableau.',
            'keywords': 'data visualization, tableau, dashboards, charts, business intelligence'
        },
        {
            'course_id': 'AI101',
            'title': 'Introduction to Artificial Intelligence',
            'department': 'Artificial Intelligence',
            'description': 'Fundamental AI concepts, search algorithms, and problem-solving.',
            'keywords': 'artificial intelligence, ai, search algorithms, problem solving'
        },
        {
            'course_id': 'AI201',
            'title': 'Natural Language Processing',
            'department': 'Artificial Intelligence',
            'description': 'Text processing, sentiment analysis, and language models.',
            'keywords': 'nlp, natural language processing, text analysis, sentiment analysis'
        },
        {
            'course_id': 'WEB101',
            'title': 'Web Development with Flask',
            'department': 'Web Development',
            'description': 'Build web applications using Python Flask framework and REST APIs.',
            'keywords': 'web development, flask, python, rest api, backend'
        },
        {
            'course_id': 'WEB201',
            'title': 'Full Stack JavaScript Development',
            'department': 'Web Development',
            'description': 'Modern JavaScript, React, Node.js, and MongoDB for full-stack applications.',
            'keywords': 'javascript, react, node.js, mongodb, full stack'
        },
        {
            'course_id': 'STAT101',
            'title': 'Statistics for Data Science',
            'department': 'Mathematics',
            'description': 'Probability, statistical inference, and hypothesis testing for data analysis.',
            'keywords': 'statistics, probability, data analysis, hypothesis testing'
        },
        {
            'course_id': 'MATH201',
            'title': 'Linear Algebra for Machine Learning',
            'department': 'Mathematics',
            'description': 'Vectors, matrices, and linear transformations with ML applications.',
            'keywords': 'linear algebra, matrices, vectors, machine learning'
        },
        {
            'course_id': 'BIO101',
            'title': 'Bioinformatics with Python',
            'department': 'Biology',
            'description': 'Python applications in biological data analysis and genomic research.',
            'keywords': 'bioinformatics, python, biology, genomics, data analysis'
        },
        {
            'course_id': 'BUS101',
            'title': 'Business Analytics',
            'department': 'Business',
            'description': 'Data-driven decision making and business intelligence tools.',
            'keywords': 'business analytics, decision making, business intelligence, data'
        },
        {
            'course_id': 'CLOUD101',
            'title': 'Cloud Computing with AWS',
            'department': 'Cloud Computing',
            'description': 'AWS services, cloud architecture, and deployment strategies.',
            'keywords': 'aws, cloud computing, cloud architecture, deployment'
        }
    ]
    
    return pd.DataFrame(courses)

def load_sample_data(app):
    """Load sample courses into CSV file"""
    df = create_sample_courses()
    data_path = os.path.join(app.config['DATA_DIR'], 'courses.csv')
    df.to_csv(data_path, index=False)
    return df

def get_courses_data(app) -> pd.DataFrame:
    """Load courses data from CSV"""
    data_path = os.path.join(app.config['DATA_DIR'], 'courses.csv')
    
    if not os.path.exists(data_path):
        df = load_sample_data(app)
    else:
        df = pd.read_csv(data_path)
    
    return df

def save_recommendation_history(db, SearchHistory, query: str, model_type: str, results: List[Dict]):
    """Save search history to database"""
    search = SearchHistory(
        query=query,
        model_type=model_type,
        results=json.dumps(results)
    )
    db.session.add(search)
    db.session.commit()
    return search.id

def save_recommendation(db, SavedRecommendation, search_id: int, course_id: str, course_data: Dict):
    """Save individual recommendation"""
    recommendation = SavedRecommendation(
        search_history_id=search_id,
        course_id=course_id,
        course_title=course_data['title'],
        course_department=course_data['department'],
        course_description=course_data['description'],
        relevance_score=course_data['relevance_score']
    )
    db.session.add(recommendation)
    db.session.commit()