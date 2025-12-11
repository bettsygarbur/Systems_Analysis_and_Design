#!/usr/bin/env python3
"""
Script de verificación: Comprueba que todos los archivos están en su lugar
y que las dependencias están instaladas correctamente.
"""

import os
import sys

def check_structure():
    """Verifica la estructura del proyecto"""
    print("\n" + "="*50)
    print("🔍 Verificando estructura del proyecto...")
    print("="*50 + "\n")
    
    required_files = [
        'app.py',
        'train_model.py',
        'preprocess.py',
        'config.py',
        'requirements.txt',
        'templates/index.html',
        'static/style.css',
        'static/script.js'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    # Crear carpeta data si no existe
    if not os.path.exists('data'):
        os.makedirs('data')
        print("\n✅ Carpeta 'data/' creada")
    else:
        print("\n✅ Carpeta 'data/' existe")
    
    return True

def check_train_data():
    """Verifica que el archivo de entrenamiento existe"""
    print("\n" + "="*50)
    print("📊 Verificando datos de entrenamiento...")
    print("="*50 + "\n")
    
    if os.path.exists('data/train.csv'):
        import pandas as pd
        try:
            df = pd.read_csv('data/train.csv')
            print(f"✅ data/train.csv encontrado")
            print(f"   Filas: {len(df)}")
            print(f"   Columnas: {len(df.columns)}")
            print(f"   Columnas: {', '.join(df.columns[:5])}...")
            
            if 'sii' in df.columns:
                print(f"✅ Columna 'sii' (target) encontrada")
                print(f"   Distribución: {df['sii'].value_counts().to_dict()}")
            else:
                print(f"❌ Columna 'sii' (target) NO encontrada")
                return False
            
            return True
        except Exception as e:
            print(f"❌ Error leyendo archivo: {str(e)}")
            return False
    else:
        print("⚠️  data/train.csv NO encontrado")
        print("   Por favor, coloca tu archivo train.csv en la carpeta 'data/'")
        return False

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("\n" + "="*50)
    print("📦 Verificando dependencias...")
    print("="*50 + "\n")
    
    required_packages = [
        'flask',
        'flask_cors',
        'catboost',
        'pandas',
        'numpy',
        'sklearn'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Instala las dependencias faltantes:")
        print(f"   pip install -r requirements.txt")
        return False
    
    return True

def main():
    print("\n🚀 VERIFICACIÓN DE PROYECTO - KAGGLE PREDICTOR\n")
    
    checks = [
        ("Estructura", check_structure),
        ("Dependencias", check_dependencies),
        ("Datos de entrenamiento", check_train_data)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error en verificación {name}: {str(e)}")
            results.append((name, False))
    
    # Resumen final
    print("\n" + "="*50)
    print("📋 RESUMEN")
    print("="*50 + "\n")
    
    all_passed = True
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("\n✅ TODO LISTO! Ejecuta: python app.py\n")
        print("La aplicación estará en: http://localhost:5000\n")
    else:
        print("\n⚠️  Hay problemas que corregir antes de ejecutar.\n")
    
    print("="*50 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
