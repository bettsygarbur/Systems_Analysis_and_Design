🎯 Kaggle Predictor – Child Mind Institute Dataset

A complete pure Python application for predicting problematic technology use using CatBoost on biometric data from the Child Mind Institute dataset.

📋 Project Structure
kaggle-predictor/
├── app.py                 # Main Flask API
├── train_model.py         # CatBoost training logic
├── preprocess.py          # Data preprocessing and cleaning
├── config.py              # Global configuration
├── requirements.txt       # Python dependencies
│
├── data/
│   └── train.csv          # Training file (must be provided)
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

Place your train.csv file inside the data/ directory:

mkdir -p data
# Copy your train.csv here
cp /path/to/your/train.csv data/

3. Run the application
python app.py


The application will start at http://localhost:5000

The first time it runs, the model will be trained automatically using all available data.

🔧 Architecture
Backend (Flask + Python)

app.py – REST API with the following endpoints:

GET / – Serves the frontend

POST /api/predict – Performs prediction and re-trains the model

GET /api/metrics – Returns current model metrics

GET /api/feature-importance – Returns top 20 most important features

train_model.py – ModelTrainer class:

Automatically trains CatBoost

Computes metrics: Accuracy, Precision, Recall, F1, ROC-AUC

Extracts feature importance

Saves/loads the model using pickle

preprocess.py – DataPreprocessor class:

Identifies categorical and numerical columns

Imputes missing values using the median strategy

Encodes categorical variables with LabelEncoder

Transforms data for the model

Frontend (Pure HTML / CSS / JS)

Drag-and-drop upload for CSV/Parquet files

Real-time visualization of model metrics

Prediction table with probabilities

Feature importance chart

CSV download of prediction results

Modern and responsive UI

📊 Usage Flow

User uploads a file (CSV or Parquet)

System trains the model using data/train.csv

Prediction is performed on the uploaded file

Results are displayed in an interactive table

Predictions can be downloaded as CSV

⚙️ Configuration

Edit config.py to adjust:

DEBUG = True                    # Debug mode
PORT = 5000                     # Server port
CATBOOST_ITERATIONS = 100       # Number of model iterations
TRAIN_TEST_SPLIT = 0.2          # (Not currently used, trains on full dataset)

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
    # Comment out this line if retraining is not desired:
    trainer.train(TRAIN_DATA_PATH)  # ← HERE

📈 Metrics Computed

Accuracy – Overall correctness

Precision – Proportion of correct positive predictions

Recall – Ability to detect positives

F1 Score – Balance between Precision and Recall

ROC-AUC – Area under the ROC curve

🎯 Expected Columns

Your dataset should include:

All biometric columns (BMI, HR, Weight, etc.)

PCIAT questionnaire columns

SDS (sleepiness scale) columns

sii column as target

0 = Non-problematic

1 = Problematic

id column for identification (optional)

🐛 Troubleshooting
Error: “File not found”

Make sure data/train.csv exists in the correct directory

Error: “Model not trained”

Restart the application using python app.py to trigger training

Slow predictions

Reduce CATBOOST_ITERATIONS in config.py

Use smaller input files for testing

📝 Example Usage
# Terminal 1: Start server
python app.py

# Terminal 2: Open browser
# Go to http://localhost:5000
# 1. Drag and drop CSV/Parquet file
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

Uses pickle to save/load models

Numerical values are imputed using median

Categorical variables are encoded with LabelEncoder

CatBoost runs with task_type='CPU'

Flask supports CORS (Cross-Origin Requests)

✅ Initial Checklist

 Python 3.8+ installed

 Dependencies installed (requirements.txt)

 data/train.csv present

 Port 5000 available

 Run python app.py

 Open http://localhost:5000

Built for the Kaggle Competition – Child Mind Institute Dataset
