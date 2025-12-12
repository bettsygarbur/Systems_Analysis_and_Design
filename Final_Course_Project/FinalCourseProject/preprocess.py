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
        self.categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        self.numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        # Excluir target e id
        if target_column in self.numeric_columns:
            self.numeric_columns.remove(target_column)
        if 'id' in self.numeric_columns:
            self.numeric_columns.remove('id')
        if 'id' in self.categorical_columns:
            self.categorical_columns.remove('id')

        # Ajustar imputador
        if self.numeric_columns:
            self.imputer.fit(df[self.numeric_columns])

        # Ajustar label encoders
        for col in self.categorical_columns:
            le = LabelEncoder()
            le.fit(df[col].fillna('missing').astype(str))
            self.label_encoders[col] = le

        self.feature_columns = self.numeric_columns + self.categorical_columns
        return self

    def transform(self, df):
        """
        Transforma los datos manteniendo el mismo esquema de columnas del entrenamiento.
        """
        df = df.copy()

        # Asegurar numéricas
        for col in self.numeric_columns:
            if col not in df.columns:
                df[col] = np.nan

        # Asegurar categóricas
        for col in self.categorical_columns:
            if col not in df.columns:
                df[col] = 'missing'

        # Imputar numéricas
        if self.numeric_columns:
            df[self.numeric_columns] = self.imputer.transform(df[self.numeric_columns])

        # Codificar categóricas
        for col in self.categorical_columns:
            le = self.label_encoders[col]
            series = df[col].fillna('missing').astype(str)
            series = series.apply(lambda x: x if x in le.classes_ else 'missing')
            df[col] = le.transform(series)

        return df[self.numeric_columns + self.categorical_columns]

    def fit_transform(self, df, target_column='sii'):
        return self.fit(df, target_column).transform(df)

    def get_feature_names(self):
        return self.feature_columns


def load_and_preprocess(data_path, target_column='sii'):
    if data_path.endswith('.csv'):
        df = pd.read_csv(data_path)
    elif data_path.endswith('.parquet'):
        df = pd.read_parquet(data_path)
    else:
        raise ValueError("Formato no soportado. Use CSV o Parquet")

    X = df.drop(columns=[target_column, 'id'], errors='ignore')
    y = df[target_column] if target_column in df.columns else None

    preprocessor = DataPreprocessor()
    X_processed = preprocessor.fit_transform(X, target_column)

    return X_processed, y, preprocessor
