# Systems Analysis & Design – Final Course Project  
## Problematic Internet Use (Child Mind Institute – Kaggle)

Este repositorio contiene el **proyecto final completo** del curso **Systems Analysis & Design**, desarrollado a partir de la competencia **Child Mind Institute – Problematic Internet Use** de Kaggle.  
El proyecto integra análisis de sistemas, diseño arquitectónico, machine learning y simulación computacional, siguiendo los Workshops 1–4 del curso.

---

## 📌 Descripción del Proyecto

El uso problemático de internet (Problematic Internet Use, PIU) en niños y adolescentes está asociado con alteraciones del sueño, dificultades emocionales y bajo desempeño académico. La detección temprana es compleja debido a la naturaleza multifactorial del problema.

Este proyecto aborda el PIU desde una **perspectiva de ingeniería de sistemas**, diseñando e implementando:

- Un **modelo predictivo** para estimar la severidad del PIU.
- Un **escenario de simulación** para analizar la evolución del problema en una población sintética.
- Una **aplicación web** que expone el modelo mediante una API REST.

La fuente de datos utilizada es la competencia oficial de Kaggle:

**Child Mind Institute – Problematic Internet Use**

---

## 🎯 Objetivo General

Diseñar e implementar un sistema que permita **predecir y analizar la severidad del uso problemático de internet** en niños y adolescentes, integrando datos clínicos, cuestionarios psicológicos y variables biométricas.

---

## 📊 Dataset y Variable Objetivo

- **Dataset:** Child Mind Institute – Problematic Internet Use (Kaggle)
- **Variable objetivo:** Severity Impairment Index (**sii**)
- **Escala ordinal:**
  - 0: No impairment
  - 1: Mild
  - 2: Moderate
  - 3: Severe
- **Tipo de problema:** Clasificación ordinal semi-supervisada
- **Métrica de evaluación:** Quadratic Weighted Kappa (QWK)

---

## 🧠 Arquitectura del Sistema

El sistema sigue una arquitectura modular basada en los Workshops del curso:

1. **Ingesta de datos**
   - Archivos CSV (datos clínicos y cuestionarios)
   - Archivos Parquet (datos de acelerometría)

2. **Preprocesamiento**
   - Limpieza y normalización
   - Manejo de valores faltantes
   - Extracción de características

3. **Escenario 1 – Predicción basada en datos**
   - Modelo de Machine Learning (CatBoost)
   - Clasificación multicategoría del sii (0–3)

4. **Escenario 2 – Simulación basada en eventos**
   - Autómata celular
   - Evolución temporal del sii en una población sintética

5. **Aplicación Web**
   - API REST implementada con Flask
   - Predicción y exportación de resultados

---

## ⚙️ Escenario 1 – Modelo Predictivo

- **Modelo utilizado:** CatBoostClassifier
- **Justificación:**
  - Manejo nativo de variables categóricas
  - Robustez ante datos faltantes
  - Buen desempeño en datos tabulares heterogéneos

El modelo predice la severidad del PIU en una escala ordinal (0–3) y también permite una clasificación binaria (normal / problemático).

---

## 🔄 Escenario 2 – Simulación (Autómata Celular)

El segundo escenario implementa una simulación basada en eventos para analizar el comportamiento del sistema a nivel poblacional.

- Cada celda representa un individuo.
- El estado corresponde al valor de `sii`.
- Las reglas de transición consideran:
  - Estado individual
  - Nivel de uso de internet
  - Influencia de vecinos
  - Componente estocástico

Este escenario permite estudiar estabilidad, sensibilidad y patrones emergentes del sistema.

---

## 🌐 Aplicación Web

El proyecto incluye una aplicación web que expone el modelo predictivo:

- **Backend:** Flask (API REST)
- **Lenguaje:** Python
- **Funcionalidades:**
  - Carga de archivos CSV y Parquet
  - Predicción del sii
  - Clasificación binaria de riesgo
  - Probabilidades y nivel de confianza
  - Descarga de resultados en CSV

---

## 📁 Estructura del Repositorio

```text
Systems_Analysis_and_Design/
│
├── Catch_up/
├── Workshops/
├── Final_Course_Project/
│   ├── FinalCourseProject/
│   ├── The_final_version_of_the_paper.pdf
│   ├── The_final_version_of_the_report.pdf
│   ├── Final Poster - Team 20.pdf
│   ├── Slides - Project Report.pdf
│
├── README.md
