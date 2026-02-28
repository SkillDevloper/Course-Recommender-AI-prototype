# Course Recommender AI prototype

An intelligent course recommendation system that compares TF-IDF (keyword-based) and Neural (semantic) models to provide personalized learning recommendations.

## 🚀 Features

- **Dual-Model Architecture**: Compare keyword-based (TF-IDF) vs semantic (Neural) recommendations
- **Natural Language Queries**: Describe learning goals in plain English
- **Professional Dashboard**: Track search history and save recommendations
- **Real-time Results**: Dynamic AJAX-based interface
- **Production-ready**: Clean, modular code with proper error handling

## Screenshots
![Home](https://github.com/SkillDevloper/Course-Recommender-AI-prototype/blob/main/Screenshots/Home%20Page.png)
![About](https://github.com/SkillDevloper/Course-Recommender-AI-prototype/blob/main/Screenshots/About%20Page.png)
![Dashboard](https://github.com/SkillDevloper/Course-Recommender-AI-prototype/blob/main/Screenshots/Dashboard%20Page.png)
![Recommendation](https://github.com/SkillDevloper/Course-Recommender-AI-prototype/blob/main/Screenshots/Recommendation%20Page.png)

## 🏗️ Architecture

```
project/
├── app.py                # Flask application factory
├── models.py             # Database models (NEW)
├── config.py             # Configuration settings
├── routes/               # View and API routes
├── ml/                   # Machine learning models
├── templates/            # HTML templates
├── static/               # CSS and JavaScript
├── create_models.py      # Model training script
└── requirements.txt      # Python dependencies
```

## Complete Project Structure

```
project/
│
├── app.py               # Flask app setup (no database models)
├── models.py            # Database models (NEW location)
├── create_models.py     # ML model initialization script
├── config.py            # Configuration settings
├── requirements.txt     # Dependencies
├── database.db          # SQLite database (auto-created)
│
├── ml/                  # Machine Learning
│   ├── __init__.py
│   ├── tfidf_model.py   # TF-IDF model
│   ├── neural_model.py  # Neural model
│   └── utils.py         # Utility functions
│
├── routes/              # Application routes
│   ├── __init__.py
│   ├── views.py         # Page routes
│   └── api.py           # API endpoints
│
├── templates/           # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── recommend.html
│   ├── dashboard.html
│   └── about.html
│
└── static/              # Static files
    ├── css/
    │   └── style.css
    └── js/
        ├── app.js
        └── recommend.js
```

## 🧠 Machine Learning Models

### TF-IDF Model
- Keyword frequency-based matching
- Scikit-learn implementation
- Fast and interpretable results

### Neural Model
- Sentence-BERT embeddings (`all-MiniLM-L6-v2`)
- Semantic similarity matching
- Context-aware recommendations

## 🛠️ Installation & Setup

The project targets **Python 3.11+** (3.14 tested). Create and activate a
virtual environment before installing anything.

1. **Clone the repository**
   ```bash
   git clone https://github.com/SkillDevloper/Course-Recommender-AI-prototype.git
   cd "Course Recommender AI prototype"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # Linux / macOS
   source venv/bin/activate
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   # Windows CMD
   venv\Scripts\activate
   ```

3. **Upgrade build tools (optional but recommended)**
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

4. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```
   > The script includes Flask, SQLAlchemy, pandas, scikit-learn, transformers,
   > torch, sentence-transformers, and other ML libraries. Installing may take
   > several minutes; do **not** cancel it.

5. **(First run) initialize the ML models**
   ```bash
   python create_models.py
   ```
   This creates TF‑IDF and neural models in `ml/models/` and a sample `courses.csv`
   in `ml/data/`. If the models are missing or outdated later, the app will
   automatically retrain them when needed.

6. **Start the Flask server**
   ```bash
   python app.py
   ```

7. **Browse the UI**
   Open `http://localhost:5000` in your browser.

---

## ⚠️ Common Issues & Troubleshooting

* **`ModuleNotFoundError` errors** – activate the venv and rerun
  `pip install -r requirements.txt`. Most missing-module problems stem from
  incomplete installs.
* **Circular import when calling `create_models.py`** – make sure routes import
  models from `models.py` (this is already fixed in the current code).
* **`TemplateAssertionError: No filter named 'fromjson'`** – upgrade to the
  latest `app.py`; it now registers a `fromjson` Jinja filter automatically.
* **`AttributeError: 'NoneType' object has no attribute 'iloc'` when calling
  `/api/recommend`** – delete any old `ml/models/tfidf_model.joblib` file and
  re-run `python create_models.py`, or simply restart the server; it will
  retrain if `courses_df` is missing.
* **Database path or secret key** – configure via environment variables in a
  `.env` file (`DATABASE_URL`, `SECRET_KEY`, `FLASK_DEBUG`, etc.). See
  `config.py` for details.
* **Windows path issues** – use forward slashes in config values or wrap paths
  in quotes. Flask’s debugger can be triggered by adding
  `?__debugger__=yes` to the URL.

If you modify the data schema or add new tables, run the app once to let
`db.create_all()` create them.

---

## 🔧 Configuration

Settings are stored in `config.py` and can be overridden using environment
variables or a `.env` file. Key settings:

* `DATABASE_URL` – SQLAlchemy database URI (defaults to `sqlite:///database.db`)
* `SECRET_KEY` – Flask session secret (must be changed in production)
* `MODEL_CACHE_DIR`, `DATA_DIR` – where trained models and CSV data are stored
* `TFIDF_MODEL_PATH`, `TFIDF_VECTORIZER_PATH` – paths used by the TF-IDF code
* `NEURAL_MODEL_NAME` – name of the HuggingFace model for semantic embeddings

Use `FLASK_DEBUG=true` to enable the debugger and auto-reload during
development.

## 📊 Usage Examples

### Sample Queries
- "I want to learn Python for data science and machine learning"
- "Web development with JavaScript frameworks"
- "Deep learning and neural networks"
- "Data analysis and visualization techniques"

### Model Comparison
| Query | TF-IDF Focus | Neural Focus |
|-------|-------------|-------------|
| "Python data science" | Python syntax, data structures | Data pipelines, ML workflows |
| "AI and machine learning" | Algorithms, techniques | Applications, ethics, future trends |

## 🔧 API Endpoints

- `POST /api/recommend` - Get course recommendations
- `GET /api/history` - Get search history
- `POST /api/save` - Save recommendations
- `GET /api/compare/<query>` - Compare models

## 🎨 UI Components

- **Home Page**: System overview and capabilities
- **Recommendations**: Query input and results display
- **Dashboard**: Analytics and saved recommendations
- **About**: System architecture and model details

## 📈 Performance Metrics

- Response time: < 2 seconds
- Accuracy: Varies by model and query type
- Scalability: Modular design supports large datasets

> The application includes all standard features of the prototype and serves as
> a clear demonstration of keyword‑based versus semantic recommender behaviour.# Course-Recommender-AI-prototype
