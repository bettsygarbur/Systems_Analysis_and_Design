from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import io
from train_model import train_model_if_needed, ModelTrainer
from preprocess import DataPreprocessor
from config import MODEL_PATH, TRAIN_DATA_PATH, PORT
import traceback

app = Flask(__name__)
CORS(app)

# Variables globales para el modelo
trainer = None
current_metrics = None

def initialize_model():
    """
    Inicializa el modelo al arrancar la aplicación
    """
    global trainer, current_metrics
    print("\n" + "="*50)
    print("🚀 Inicializando aplicación...")
    print("="*50)
    
    trainer = train_model_if_needed(MODEL_PATH, TRAIN_DATA_PATH)
    current_metrics = trainer.metrics
    
    print("\n✅ Aplicación lista en http://localhost:5000")
    print("="*50 + "\n")

# Rutas Frontend
@app.route('/')
def index():
    """
    Sirve la página principal
    """
    return render_template('index.html')

# Rutas API
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """
    Retorna métricas del modelo actual
    """
    try:
        if trainer is None or not trainer.metrics:
            return jsonify({'error': 'Modelo no entrenado'}), 400
        
        return jsonify({
            'status': 'success',
            'metrics': trainer.metrics
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feature-importance', methods=['GET'])
def get_feature_importance():
    """
    Retorna importancia de características
    """
    try:
        if trainer is None or trainer.model is None:
            return jsonify({'error': 'Modelo no entrenado'}), 400
        
        importance = trainer.get_feature_importance()
        
        if importance is None:
            return jsonify({'error': 'No se pudo obtener importancia'}), 400
        
        features = [item[0] for item in importance]
        values = [float(item[1]) for item in importance]
        
        return jsonify({
            'status': 'success',
            'features': features,
            'importance': values
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Realiza predicción con un archivo CSV/Parquet
    """
    try:
        # Validar archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        # Leer archivo
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(file.read()))
            elif file.filename.endswith('.parquet'):
                df = pd.read_parquet(io.BytesIO(file.read()))
            else:
                return jsonify({'error': 'Formato no soportado. Use CSV o Parquet'}), 400
        except Exception as e:
            return jsonify({'error': f'Error leyendo archivo: {str(e)}'}), 400
        
        # REENTRENAMIENTO DEL MODELO
        print(f"\n🔄 Reentrenando modelo con {len(df)} registros...")
        success, result = trainer.train(TRAIN_DATA_PATH)
        
        if not success:
            print(f"⚠️  Advertencia: Entrenamiento falló: {result}")
            # No retornar error, continuar con modelo anterior si existe
            if trainer.model is None:
                return jsonify({
                    'error': f'No se pudo entrenar el modelo: {result}'
                }), 500
        else:
            print(f"✅ Modelo reentrenado exitosamente")
        
        # Verificar que el modelo existe
        if trainer.model is None:
            return jsonify({
                'error': 'Modelo no está entrenado. Verifique que data/train.csv es válido y contiene la columna "sii"'
            }), 500
        
        # Preprocesar datos
        print(f"📊 Preprocesando {len(df)} registros...")
        try:
            X_processed = trainer.preprocessor.transform(
                df.drop(columns=['id', 'sii'], errors='ignore')
            )
        except Exception as e:
            print(f"❌ Error preprocesando: {str(e)}")
            return jsonify({
                'error': f'Error en preprocesamiento: {str(e)}. Verifique que el archivo tiene las columnas esperadas.'
            }), 400
        
        # Predicción
        try:
            predictions, probabilities = trainer.predict(X_processed)
        except Exception as e:
            print(f"❌ Error en predicción: {str(e)}")
            return jsonify({
                'error': f'Error en predicción: {str(e)}'
            }), 500
        
        # Preparar respuesta
        results = []
        for i, (pred, probs) in enumerate(zip(predictions, probabilities)):
            results.append({
                'id': df['id'].iloc[i] if 'id' in df.columns else i,
                'prediction': int(pred),
                'probability_class_0': float(probs[0]) if len(probs) > 0 else 0.0,
                'probability_class_1': float(probs[1]) if len(probs) > 1 else float(probs[0]),
                'confidence': float(max(probs))
            })
        
        return jsonify({
            'status': 'success',
            'predictions': results,
            'model_metrics': trainer.metrics,
            'records_processed': len(results)
        })
        
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """
    Verifica estado de la API
    """
    return jsonify({
        'status': 'healthy',
        'model_trained': trainer is not None and trainer.model is not None
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    # Crear directorio data si no existe
    os.makedirs('data', exist_ok=True)
    
    # Inicializar modelo
    initialize_model()
    
    # Ejecutar servidor
    app.run(debug=True, port=PORT, use_reloader=False)
