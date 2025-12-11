import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import warnings

warnings.filterwarnings('ignore')

class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.imputer = SimpleImputer(strategy='median')
        self.feature_columns = None
        self.categorical_columns = None
        self.numeric_columns = None

    def fit(self, df, target_column='sii'):
        """
        Ajusta el preprocesador con los datos de entrenamiento
        """
        # Identificar columnas categóricas y numéricas
        self.categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        self.numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        # Excluir el target y id de las características
        if target_column in self.numeric_columns:
            self.numeric_columns.remove(target_column)
        if 'id' in self.numeric_columns:
            self.numeric_columns.remove('id')
        if 'id' in self.categorical_columns:
            self.categorical_columns.remove('id')
        
        # Ajustar imputador
        if self.numeric_columns:
            self.imputer.fit(df[self.numeric_columns])
        
        # Ajustar label encoders para categóricas
        for col in self.categorical_columns:
            le = LabelEncoder()
            le.fit(df[col].fillna('missing'))
            self.label_encoders[col] = le
        
        self.feature_columns = self.numeric_columns + self.categorical_columns
        return self

    def transform(self, df):
        """
        Transforma los datos
        """
        df = df.copy()
        
        # Filtrar solo las columnas que existen en ambos (entrenamiento y predicción)
        # Esto maneja archivos con columnas diferentes
        available_numeric = [col for col in self.numeric_columns if col in df.columns]
        available_categorical = [col for col in self.categorical_columns if col in df.columns]
        
        # Imputar valores numéricos faltantes
        if available_numeric:
            df[available_numeric] = self.imputer.transform(df[available_numeric])
        
        # Codificar variables categóricas
        for col in available_categorical:
            if col in self.label_encoders:
                try:
                    df[col] = self.label_encoders[col].transform(
                        df[col].fillna('missing')
                    )
                except ValueError:
                    # Si hay valores nuevos no vistos en entrenamiento
                    df[col] = self.label_encoders[col].transform(
                        df[col].fillna('missing').apply(
                            lambda x: x if x in self.label_encoders[col].classes_ else 'missing'
                        )
                    )
        
        # Retornar solo columnas disponibles (mantener orden)
        return df[available_numeric + available_categorical]

    def fit_transform(self, df, target_column='sii'):
        """
        Ajusta y transforma en un paso
        """
        return self.fit(df, target_column).transform(df)

    def get_feature_names(self):
        """
        Retorna nombres de características
        """
        return self.feature_columns

def load_and_preprocess(data_path, target_column='sii'):
    """
    Carga y preprocesa los datos
    """
    # Detectar formato
    if data_path.endswith('.csv'):
        df = pd.read_csv(data_path)
    elif data_path.endswith('.parquet'):
        df = pd.read_parquet(data_path)
    else:
        raise ValueError("Formato no soportado. Use CSV o Parquet")
    
    # Separar features y target
    X = df.drop(columns=[target_column, 'id'], errors='ignore')
    y = df[target_column] if target_column in df.columns else None
    
    # Preprocesar
    preprocessor = DataPreprocessor()
    X_processed = preprocessor.fit_transform(X, target_column)
    
    return X_processed, y, preprocessor
