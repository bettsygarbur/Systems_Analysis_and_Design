import os
import pickle
import warnings

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from preprocess import DataPreprocessor
from config import MODEL_PATH, TRAIN_DATA_PATH, CATBOOST_ITERATIONS

warnings.filterwarnings("ignore")


class ModelTrainer:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.metrics = {}
        self.feature_names = []

    def train(self, data_path=TRAIN_DATA_PATH):
        """
        Train CatBoost model using labeled rows (sii not NaN).
        """
        try:
            print(f"📥 Loading training data from {data_path}...")
            df = pd.read_csv(data_path)

            if "sii" not in df.columns:
                return False, 'Training file must contain column "sii".'

            # Use only labeled rows
            labeled = df.dropna(subset=["sii"]).copy()
            labeled["sii"] = labeled["sii"].astype(int)

            # Features
            X_raw = labeled.drop(columns=["sii", "id"], errors="ignore")
            y = labeled["sii"]

            print(f"✅ Labeled data: {X_raw.shape}")
            print(f"📊 Target distribution: {y.value_counts().to_dict()}")

            # Preprocess
            self.preprocessor = DataPreprocessor()
            X = self.preprocessor.fit_transform(X_raw)

            # Save feature names for feature importance
            self.feature_names = list(X.columns)

            # Train model
            print(f"\n🤖 Training CatBoost (iterations: {CATBOOST_ITERATIONS})...")
            self.model = CatBoostClassifier(
                iterations=CATBOOST_ITERATIONS,
                verbose=False,
                random_state=42,
                task_type="CPU",
                allow_writing_files=False
            )
            self.model.fit(X, y)

            # Evaluate (simple: on training set, consistent with your current app flow)
            y_pred = self.model.predict(X)

            self.metrics = {
                "accuracy": float(accuracy_score(y, y_pred)),
                "precision": float(self._safe_precision(y, y_pred)),
                "recall": float(self._safe_recall(y, y_pred)),
                "f1": float(self._safe_f1(y, y_pred)),
                "roc_auc": 0.0  # kept as 0.0 to avoid multi-class ROC issues
            }

            print("\n📈 Model metrics:")
            for metric, value in self.metrics.items():
                print(f"   {metric}: {value:.4f}")

            # Save model
            self.save_model(MODEL_PATH)
            print(f"\n✅ Model saved at {MODEL_PATH}")

            return True, self.metrics

        except Exception as e:
            print(f"❌ Training error: {str(e)}")
            import traceback
            traceback.print_exc()
            self.model = None
            return False, str(e)

    def _safe_precision(self, y_true, y_pred):
        try:
            return precision_score(y_true, y_pred, average="weighted", zero_division=0)
        except TypeError:
            return precision_score(y_true, y_pred, average="weighted")
        except Exception:
            return 0.0

    def _safe_recall(self, y_true, y_pred):
        try:
            return recall_score(y_true, y_pred, average="weighted", zero_division=0)
        except TypeError:
            return recall_score(y_true, y_pred, average="weighted")
        except Exception:
            return 0.0

    def _safe_f1(self, y_true, y_pred):
        try:
            return f1_score(y_true, y_pred, average="weighted", zero_division=0)
        except TypeError:
            return f1_score(y_true, y_pred, average="weighted")
        except Exception:
            return 0.0

    def predict(self, X):
        """
        Predict using already-preprocessed features (DataFrame).
        Returns (predictions, probabilities).
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")

        predictions = self.model.predict(X)

        try:
            probabilities = self.model.predict_proba(X)
        except Exception as e:
            print(f"⚠️  Error getting probabilities: {e}")
            # Fallback: create fake probs (won't happen normally)
            probabilities = np.zeros((len(predictions), 4), dtype=float)
            for i, p in enumerate(predictions):
                probabilities[i, int(p)] = 1.0

        return predictions, probabilities

    def get_feature_importance(self):
        """
        Return top 20 feature importances.
        """
        if self.model is None:
            return None

        try:
            importances = self.model.get_feature_importance()
            names = self.feature_names if self.feature_names else [f"f{i}" for i in range(len(importances))]

            pairs = list(zip(names, importances))
            pairs.sort(key=lambda x: x[1], reverse=True)

            return pairs[:20]
        except Exception as e:
            print(f"⚠️  Error getting feature importance: {e}")
            return None

    def save_model(self, path):
        with open(path, "wb") as f:
            pickle.dump(
                {
                    "model": self.model,
                    "preprocessor": self.preprocessor,
                    "metrics": self.metrics,
                    "feature_names": self.feature_names
                },
                f
            )

    def load_model(self, path):
        with open(path, "rb") as f:
            data = pickle.load(f)
            self.model = data["model"]
            self.preprocessor = data["preprocessor"]
            self.metrics = data.get("metrics", {})
            self.feature_names = data.get("feature_names", [])
        return True


def train_model_if_needed(train_csv_path=TRAIN_DATA_PATH, model_path=MODEL_PATH):
    """
    This matches app.py expectations:
    returns (success: bool, trainer_or_message)
    """
    trainer = ModelTrainer()

    if os.path.exists(model_path):
        try:
            print("✅ Model found. Loading...")
            trainer.load_model(model_path)
            return True, trainer
        except Exception:
            print("⚠️ Model load failed. Retraining...")

    print("📦 Model not found. Training a new one...")
    ok, res = trainer.train(train_csv_path)
    if not ok:
        return False, res

    return True, trainer


if __name__ == "__main__":
    ok, result = train_model_if_needed(TRAIN_DATA_PATH, MODEL_PATH)
    if not ok:
        print(result)
