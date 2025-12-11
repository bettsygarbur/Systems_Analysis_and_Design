import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_PATH = os.path.join(DATA_DIR, 'model.pkl')
TRAIN_DATA_PATH = os.path.join(DATA_DIR, 'train.csv')

# Configuración Flask
DEBUG = True
PORT = 5000

# Configuración CatBoost
CATBOOST_ITERATIONS = 100
CATBOOST_VERBOSE = False
TRAIN_TEST_SPLIT = 0.2

# Columnas a usar
TARGET_COLUMN = 'sii'
ID_COLUMN = 'id'
SEASON_COLUMNS = [col for col in [] if 'Season' in col]  # Se rellenarán dinámicamente
