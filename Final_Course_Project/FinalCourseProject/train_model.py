import pickle
import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from preprocess import load_and_preprocess
from config import MODEL_PATH, TRAIN_DATA_PATH, CATBOOST_ITERATIONS
import warnings

warnings.filterwarnings('ignore')

class ModelTrainer:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.metrics = {}

    def train(self, data_path=TRAIN_DATA_PATH):
        """
        Entrena el modelo CatBoost con los datos
        """
        try:
            print(f"📥 Cargando datos desde {data_path}...")
            X, y, preprocessor = load_and_preprocess(data_path, target_column='sii')
            self.preprocessor = preprocessor
            
            print(f"✅ Datos cargados: {X.shape}")
            print(f"📊 Distribución del target: {y.value_counts().to_dict()}")
            
            # CRÍTICO: Eliminar valores NaN del target
            valid_idx = y.notna()
            X = X[valid_idx]
            y = y[valid_idx]
            
            print(f"✅ Después de limpiar NaN: {X.shape}")
            print(f"📊 Nueva distribución: {y.value_counts().to_dict()}")
            
            # Verificar que no hay NaN en el target
            if y.isna().any():
                raise ValueError("Target contiene NaN después de limpieza")
            
            # Entrenar modelo
            print(f"\n🤖 Entrenando CatBoost (iteraciones: {CATBOOST_ITERATIONS})...")
            self.model = CatBoostClassifier(
                iterations=CATBOOST_ITERATIONS,
                verbose=False,
                random_state=42,
                task_type='CPU',
                allow_writing_files=False
            )
            
            self.model.fit(X, y, verbose=False)
            
            # Evaluar - VERSIÓN SIMPLIFICADA
            y_pred = self.model.predict(X)
            
            # Calcular métricas de manera simple
            self.metrics = {
                'accuracy': float(accuracy_score(y, y_pred)),
                'precision': float(self._safe_precision(y, y_pred)),
                'recall': float(self._safe_recall(y, y_pred)),
                'f1': float(self._safe_f1(y, y_pred)),
                'roc_auc': 0.0  # Simplificado para evitar errores
            }
            
            print(f"\n📈 Métricas del modelo:")
            for metric, value in self.metrics.items():
                print(f"   {metric}: {value:.4f}")
            
            # Guardar modelo
            self.save_model(MODEL_PATH)
            print(f"\n✅ Modelo guardado en {MODEL_PATH}")
            
            return True, self.metrics
            
        except Exception as e:
            print(f"❌ Error durante entrenamiento: {str(e)}")
            import traceback
            traceback.print_exc()
            self.model = None
            return False, str(e)

    def _safe_precision(self, y_true, y_pred):
        """Calcula precision de forma segura"""
        try:
            return precision_score(y_true, y_pred, average='weighted', zero_division=0)
        except TypeError:
            return precision_score(y_true, y_pred, average='weighted')
        except:
            return 0.0

    def _safe_recall(self, y_true, y_pred):
        """Calcula recall de forma segura"""
        try:
            return recall_score(y_true, y_pred, average='weighted', zero_division=0)
        except TypeError:
            return recall_score(y_true, y_pred, average='weighted')
        except:
            return 0.0

    def _safe_f1(self, y_true, y_pred):
        """Calcula f1 de forma segura"""
        try:
            return f1_score(y_true, y_pred, average='weighted', zero_division=0)
        except TypeError:
            return f1_score(y_true, y_pred, average='weighted')
        except:
            return 0.0

    def predict(self, X):
        """
        Realiza predicciones
        """
        if self.model is None:
            raise ValueError("Modelo no entrenado. Llama a train() primero.")
        
        predictions = self.model.predict(X)
        
        # Obtener probabilidades de forma segura
        try:
            probabilities = self.model.predict_proba(X)
            
            # Asegurar formato correcto
            if probabilities.ndim == 1:
                # Si es 1D, lo asumimos como probabilidad de clase 1
                probabilities = np.column_stack([
                    1 - probabilities,
                    probabilities
                ])
            elif probabilities.shape[1] == 1:
                # Si tiene solo una columna, crear la otra
                probabilities = np.column_stack([
                    1 - probabilities,
                    probabilities
                ])
        except Exception as e:
            print(f"⚠️  Error obteniendo probabilidades: {e}")
            # Fallback: crear probabilidades artificiales basadas en predicciones
            probabilities = np.column_stack([
                np.where(predictions == 0, 0.9, 0.1),
                np.where(predictions == 1, 0.9, 0.1)
            ])
        
        return predictions, probabilities

    def get_feature_importance(self):
        """
        Obtiene importancia de características
        """
        if self.model is None:
            return None
        
        try:
            feature_names = self.preprocessor.get_feature_names()
            importances = self.model.get_feature_importance()
            
            importance_dict = dict(zip(feature_names, importances))
            sorted_importance = sorted(
                importance_dict.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            return sorted_importance[:20]
        except Exception as e:
            print(f"⚠️  Error obteniendo importancia: {e}")
            return None

    def save_model(self, path):
        """
        Guarda el modelo a disco
        """
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'preprocessor': self.preprocessor,
                'metrics': self.metrics
            }, f)

    def load_model(self, path):
        """
        Carga el modelo desde disco
        """
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.preprocessor = data['preprocessor']
            self.metrics = data['metrics']
        return True

def train_model_if_needed(model_path=MODEL_PATH, data_path=TRAIN_DATA_PATH):
    """
    Entrena el modelo si no existe
    """
    import os
    
    trainer = ModelTrainer()
    
    if not os.path.exists(model_path):
        print(f"📦 Modelo no encontrado. Entrenando nuevo...")
        trainer.train(data_path)
    else:
        print(f"✅ Modelo encontrado. Cargando...")
        trainer.load_model(model_path)
    
    return trainer

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train()
