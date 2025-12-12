# 🎯 Kaggle Predictor - Child Mind Institute Dataset

Aplicación completa en **Python puro** para predicción de uso problemático de tecnología usando **CatBoost** en datos biométricos del Child Mind Institute.

## 📋 Estructura del Proyecto

```
kaggle-predictor/
├── app.py                 # API Flask principal
├── train_model.py         # Lógica de entrenamiento CatBoost
├── preprocess.py          # Preprocesamiento y limpieza de datos
├── config.py              # Configuración global
├── requirements.txt       # Dependencias Python
│
├── data/
│   └── train.csv          # Archivo de entrenamiento (debes agregarlo)
│
├── templates/
│   └── index.html         # Frontend HTML
│
└── static/
    ├── style.css          # Estilos CSS
    └── script.js          # Lógica JavaScript
```

## 🚀 Instalación y Ejecución

### 1. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

### 2. **Agregar datos de entrenamiento**

Coloca tu archivo `train.csv` en la carpeta `data/`:

```bash
mkdir -p data
# Copia tu train.csv aquí
cp /ruta/a/tu/train.csv data/
```

### 3. **Ejecutar la aplicación**

```bash
python app.py
```

La aplicación se iniciará en `http://localhost:5000`

La **primera vez** que ejecutes, entrenará automáticamente el modelo con todos los datos.

## 🔧 Arquitectura

### Backend (Flask + Python)

**`app.py`** - API REST con endpoints:
- `GET /` - Sirve el frontend
- `POST /api/predict` - Realiza predicción y **reentrana el modelo**
- `GET /api/metrics` - Retorna métricas del modelo actual
- `GET /api/feature-importance` - Retorna top 20 características importantes

**`train_model.py`** - Clase `ModelTrainer`:
- Entrena CatBoost automáticamente
- Calcula métricas: Accuracy, Precision, Recall, F1, ROC-AUC
- Obtiene importancia de características
- Guarda/carga modelo en pickle

**`preprocess.py`** - Clase `DataPreprocessor`:
- Identifica columnas categóricas y numéricas
- Imputa valores faltantes con estrategia 'median'
- Codifica variables categóricas con LabelEncoder
- Transforma datos para el modelo

### Frontend (HTML/CSS/JS puro)

- **Upload drag-and-drop** de archivos CSV/Parquet
- **Visualización de métricas** del modelo en tiempo real
- **Tabla de predicciones** con probabilidades
- **Gráfico de importancia** de características
- **Descarga de resultados** en CSV
- Interfaz **responsiva** y moderna

## 📊 Flujo de Uso

1. **Usuario sube archivo** (CSV o Parquet)
2. **Sistema entrena modelo** con los datos de `data/train.csv`
3. **Predicción en archivo subido**
4. **Visualización de resultados** en tabla interactiva
5. **Descarga de predicciones** en CSV

## ⚙️ Configuración

Edita `config.py` para ajustar:

```python
DEBUG = True                    # Modo debug
PORT = 5000                     # Puerto del servidor
CATBOOST_ITERATIONS = 100       # Número de iteraciones del modelo
TRAIN_TEST_SPLIT = 0.2          # (No usado actualmente, entrena con todo)
```

## 📦 Dependencias

- **Flask** - Framework web
- **CatBoost** - Modelo de gradiente boosting
- **Pandas** - Manipulación de datos
- **Scikit-learn** - Preprocesamiento y métricas

## 🔄 Reentrenamiento

**Importante**: Cada vez que realizas una predicción, el modelo se **reentrana completamente** con los datos de `data/train.csv`.

Para cambiar esto, edita en `app.py`:

```python
@app.route('/api/predict', methods=['POST'])
def predict():
    # ...
    # Comentar estas líneas si no quieres reentrenar:
    trainer.train(TRAIN_DATA_PATH)  # ← AQUÍ
```

## 📈 Métricas Calculadas

- **Accuracy** - Exactitud general del modelo
- **Precision** - Proporción de positivos correctos
- **Recall** - Capacidad de detectar positivos
- **F1 Score** - Balance entre Precision y Recall
- **ROC-AUC** - Área bajo la curva ROC

## 🎯 Columnas Esperadas

Tu archivo debe incluir:
- Todas las columnas biométricas (BMI, HR, Weight, etc.)
- Columnas PCIAT (cuestionario de uso de internet)
- Columnas SDS (escala de somnolencia)
- Columna **`sii`** como target (0 = No problemático, 1 = Problemático)
- Columna **`id`** para identificación (opcional)

## 🐛 Troubleshooting

### Error: "Archivo no encontrado"
- Verifica que `data/train.csv` existe en la carpeta correcta

### Error: "Modelo no entrenado"
- Ejecuta `python app.py` de nuevo para entrenar inicialmente

### Predicción lenta
- Reduce `CATBOOST_ITERATIONS` en `config.py`
- Usa muestras más pequeñas en tus archivos de prueba

## 📝 Ejemplo de Uso

```bash
# Terminal 1: Iniciar servidor
python app.py

# Terminal 2: Abrir navegador
# Ir a http://localhost:5000
# 1. Arrastrar archivo CSV/Parquet
# 2. Click en "Realizar Predicción"
# 3. Ver resultados en tabla
# 4. Descargar CSV con resultados
```

## 🎨 Personalización

### Cambiar colores
Edita las variables CSS en `static/style.css`:
```css
:root {
    --primary-color: #2563eb;  /* Azul principal */
    --success-color: #10b981;  /* Verde */
    --danger-color: #ef4444;   /* Rojo */
}
```

### Cambiar texto
Edita `templates/index.html` directamente

## 📞 Notas Técnicas

- Usa **pickle** para guardar/cargar modelos
- Los valores numéricos se imputan con **mediana**
- Las categorías se codifican con **LabelEncoder**
- CatBoost se configura con `task_type='CPU'`
- Flask permite CORS (Cross-Origin Requests)

## ✅ Checklist Inicial

- [ ] Python 3.8+ instalado
- [ ] `requirements.txt` instalado
- [ ] `data/train.csv` en carpeta `data/`
- [ ] Puerto 5000 disponible
- [ ] Ejecutar `python app.py`
- [ ] Abrir `http://localhost:5000`

---

**Creado para Kaggle Competition - Child Mind Institute Dataset**
