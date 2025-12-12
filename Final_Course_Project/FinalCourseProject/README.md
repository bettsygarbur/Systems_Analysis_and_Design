🎯 Kaggle Predictor – Child Mind Institute Dataset

A complete pure Python application for predicting problematic technology use using CatBoost on Child Mind Institute biometric data.

📋 Project Structure
kaggle-predictor/
├── app.py                 # Main Flask API
├── train_model.py         # CatBoost training logic
├── preprocess.py          # Data preprocessing and cleaning
├── config.py              # Global configuration
├── requirements.txt       # Python dependencies
│
├── data/
│   └── train.csv          # Training file (you must add it)
│
├── templates/
│   └── index.html         # HTML frontend
│
└── static/
    ├── style.css          # CSS styles
    └── script.js          # JavaScript logic

🚀 Installation and Execution
1. Install dependencies
pip install -r requirements.txt

2. Add training data

Place your train.csv file inside the data/ folder:

mkdir -p data
# Copy your train.csv here
cp /path/to/your/train.csv data/

3. Run the application
python app.py


The application will start at http://localhost:5000

The first time you run it, the model will automatically train using the full dataset.

🔧 Architecture
Backend (Flask + Python)

app.py – REST API with endpoints:

GET / – Serves the frontend

POST /api/predict – Runs prediction and re-trains the model

GET /api/metrics – Returns current model metrics

GET /api/feature-importance – Returns top 20 feature importances

train_model.py – ModelTrainer class:

Automatically trains CatBoost

Computes metrics: Accuracy, Precision, Recall, F1, ROC-AUC

Extracts feature importance

Saves/loads the model using pickle

preprocess.py – DataPreprocessor class:

Detects categorical and numerical columns

Imputes missing values using the median strategy

Encodes categorical variables with LabelEncoder

Transforms data for model consumption

Frontend (Pure HTML/CSS/JS)

Drag-and-drop upload for CSV/Parquet files

Real-time visualization of model metrics

Prediction table with probabilities

Feature importance chart

Downloadable CSV results

Modern and responsive interface

📊 Usage Flow

User uploads a file (CSV or Parquet)

System trains the model using data/train.csv

Predictions are generated for the uploaded file

Results are displayed in an interactive table

Predictions can be downloaded as CSV

⚙️ Configuration

Edit config.py to adjust:

DEBUG = True                    # Debug mode
PORT = 5000                     # Server port
CATBOOST_ITERATIONS = 100       # Number of model iterations
TRAIN_TEST_SPLIT = 0.2          # (Currently unused – trains on full data)

📦 Dependencies

Flask – Web framework

CatBoost – Gradient boosting model

Pandas – Data manipulation

Scikit-learn – Preprocessing and metrics

🔄 Retraining Behavior

Important: Every time a prediction is made, the model is fully retrained using data/train.csv.

To disable this behavior, edit app.py:

@app.route('/api/predict', methods=['POST'])
def predict():
    # ...
    # Comment out this line if you do NOT want retraining:
    trainer.train(TRAIN_DATA_PATH)  # ← HERE

📈 Computed Metrics

Accuracy – Overall correctness

Precision – Proportion of correct positive predictions

Recall – Ability to detect positives

F1 Score – Balance between Precision and Recall

ROC-AUC – Area under the ROC curve

🎯 Expected Columns

Your dataset should include:

All biometric columns (BMI, HR, Weight, etc.)

PCIAT columns (internet usage questionnaire)

SDS columns (sleepiness scale)

sii column as target (0 = Non-problematic, 1 = Problematic)

id column for identification (optional)

🐛 Troubleshooting
Error: "File not found"

Ensure data/train.csv exists in the correct directory

Error: "Model not trained"

Run python app.py again to perform initial training

Slow predictions

Reduce CATBOOST_ITERATIONS in config.py

Use smaller test files

📝 Example Usage
# Terminal 1: Start server
python app.py

# Terminal 2: Open browser
# Go to http://localhost:5000
# 1. Drag & drop CSV/Parquet file
# 2. Click "Run Prediction"
# 3. View results in table
# 4. Download CSV with predictions

🎨 Customization
Change colors

Edit CSS variables in static/style.css:

:root {
    --primary-color: #2563eb;  /* Primary blue */
    --success-color: #10b981;  /* Green */
    --danger-color: #ef4444;   /* Red */
}

Change text

Edit templates/index.html directly

📞 Technical Notes

Uses pickle for model persistence

Numerical values are imputed using median

Categorical values are encoded with LabelEncoder

CatBoost runs with task_type='CPU'

Flask allows CORS (Cross-Origin Requests)

✅ Initial Checklist

 Python 3.8+ installed

 requirements.txt installed

 data/train.csv present in data/

 Port 5000 available

 Run python app.py

 Open http://localhost:5000

Built for Kaggle Competition – Child Mind Institute Dataset
