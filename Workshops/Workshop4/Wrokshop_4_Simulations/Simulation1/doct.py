import pandas as pd
import numpy as np

from catboost import CatBoostClassifier

# =====================================================
# 1. Cargar datos
# =====================================================
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

print("Shapes cargados:")
print("train:", train.shape)
print("test:", test.shape)

# =====================================================
# 2. Crear target multiclase
# =====================================================
def clasificar_pciat(valor):
    if valor <= 20: 
        return 0
    elif valor <= 49:
        return 1
    elif valor <= 79:
        return 2
    return 3

train["sii"] = train["PCIAT-PCIAT_Total"].apply(clasificar_pciat)

y = train["sii"]
X = train.drop(columns=["sii"])

print("\nShapes tras limpiar target:")
print("X:", X.shape)
print("y:", y.shape)

# =====================================================
# 3. Alinear columnas con test
# =====================================================
for col in X.columns:
    if col not in test.columns:
        test[col] = np.nan

test = test[X.columns]

print("\nColumnas alineadas entre train y test.")

# =====================================================
# 4. Detectar categóricas
# =====================================================
cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

print("\nCategóricas detectadas:", cat_cols)

# =====================================================
# *** SOLUCIÓN: CatBoost NO acepta NaN en categóricas ***
# Convertimos NaN a string "missing"
# =====================================================
for col in cat_cols:
    X[col] = X[col].astype(str).fillna("missing")
    test[col] = test[col].astype(str).fillna("missing")

# =====================================================
# 5. Modelo CatBoost (corregido para tu versión)
# =====================================================

from sklearn.utils.class_weight import compute_class_weight

clases = np.unique(y)
pesos = compute_class_weight(class_weight="balanced", classes=clases, y=y)
class_weights = dict(zip(clases, pesos))

print("Pesos calculados:", class_weights)

modelo = CatBoostClassifier(
    iterations=1200,
    learning_rate=0.04,
    depth=8,
    loss_function='MultiClass',
    eval_metric='TotalF1',
    class_weights=class_weights,  # 👍 esto sí funciona en todas las versiones
    random_seed=42,
    verbose=200
)


# =====================================================
# 6. Entrenar
# =====================================================
print("\nEntrenando modelo CatBoost...")
modelo.fit(X, y, cat_features=cat_cols)
print("Modelo entrenado con éxito.")

# =====================================================
# 7. Predicciones finales
# =====================================================
print("\nRealizando predicciones en test.csv...")
pred = modelo.predict(test)

salida = pd.DataFrame({
    "id": test["id"],
    "sii_predicho": pred.flatten()
})

salida.to_csv("predicciones.csv", index=False)

print("Archivo predicciones.csv generado correctamente.")
