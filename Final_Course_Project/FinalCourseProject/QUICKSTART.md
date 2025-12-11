# ⚡ QUICK START - Kaggle Predictor

## 🎯 Inicio Rápido (5 minutos)

### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Agregar archivo de datos
```bash
# Coloca tu train.csv en esta carpeta:
mkdir -p data
cp /ruta/a/tu/train.csv data/
```

### Paso 3: Ejecutar la aplicación
```bash
python app.py
```

### Paso 4: Abrir en navegador
```
http://localhost:5000
```

---

## 📁 Archivos Generados

### Backend
- **`app.py`** - Servidor Flask con API REST
- **`train_model.py`** - Entrenamiento de CatBoost
- **`preprocess.py`** - Limpieza y transformación de datos
- **`config.py`** - Configuración centralizada

### Frontend
- **`templates/index.html`** - Página principal
- **`static/style.css`** - Estilos personalizados
- **`static/script.js`** - Lógica de interfaz

### Configuración
- **`requirements.txt`** - Dependencias Python
- **`README.md`** - Documentación completa
- **`verify.py`** - Script de verificación

---

## 🔧 Primeros Pasos

### Verificar instalación
```bash
python verify.py
```

### Ver logs mientras se entrena
El terminal mostrará:
```
📥 Cargando datos desde data/train.csv...
✅ Datos cargados: (1500, 94)
📊 Distribución del target: {0: 1000, 1: 500}

🤖 Entrenando CatBoost (iteraciones: 100)...

📈 Métricas del modelo:
   accuracy: 0.8532
   precision: 0.8234
   recall: 0.7891
   f1: 0.8060
   roc_auc: 0.9123

✅ Modelo guardado en data/model.pkl

✅ Aplicación lista en http://localhost:5000
```

---

## 📊 Usando la Aplicación

1. **Subir archivo**: Arrastra tu CSV o Parquet
2. **Predicción**: Click en "Realizar Predicción"
3. **Reentrenamiento**: El modelo se reentrana automáticamente
4. **Resultados**: Tabla con predicciones y probabilidades
5. **Descargar**: CSV con todas las predicciones

---

## 🎨 Cambios Rápidos

### Cambiar iteraciones del modelo
Edita `config.py`:
```python
CATBOOST_ITERATIONS = 200  # Aumentar para más precisión (más lento)
```

### Cambiar puerto
Edita `config.py`:
```python
PORT = 8080  # O el puerto que prefieras
```

### Deshabilitar reentrenamiento
Edita `app.py`, línea 70:
```python
# Comentar estas líneas:
# trainer.train(TRAIN_DATA_PATH)
```

---

## 🐛 Problemas Comunes

### Error: "No such file or directory: 'data/train.csv'"
**Solución**: Coloca tu archivo en la carpeta `data/`

### Error: "ModuleNotFoundError: No module named 'catboost'"
**Solución**: `pip install -r requirements.txt`

### Puerto 5000 ocupado
**Solución**: Cambiar PORT en `config.py` o liberar el puerto

### Predicción muy lenta
**Solución**: Reduce `CATBOOST_ITERATIONS` a 50

---

## 📈 Próximos Pasos

1. **Entrenamiento**: El modelo se entrena la primera vez que ejecutas
2. **Predicción**: Sube un archivo para obtener predicciones
3. **Evaluación**: Revisa métricas en tiempo real
4. **Exportar**: Descarga resultados en CSV

---

## 💡 Notas Técnicas

- **Framework**: Flask (Python web framework)
- **Modelo**: CatBoost (Gradient Boosting)
- **Datos**: CSV/Parquet automáticamente detectado
- **Frontend**: HTML/CSS/JavaScript puro (sin frameworks)
- **API**: REST endpoints JSON

---

## ✨ Características

✅ Upload de archivos CSV/Parquet  
✅ Reentrenamiento automático  
✅ Métricas en tiempo real (Accuracy, Precision, Recall, F1, ROC-AUC)  
✅ Top 20 características importantes  
✅ Tabla de predicciones con probabilidades  
✅ Descarga de resultados CSV  
✅ Interfaz responsiva  
✅ Sin dependencias externas para frontend  

---

**🚀 Ready to go!**
