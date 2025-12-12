# Systems Analysis & Design – Final Course Project
## Problematic Internet Use (Child Mind Institute – Kaggle)

This repository contains the complete final project for the Systems Analysis & Design course, developed based on the Child Mind Institute – Problematic Internet Use Kaggle competition.  
The project integrates systems analysis, architectural design, machine learning, and computational simulation, following Workshops 1–4 of the course.

---

## Project Description

Problematic Internet Use (PIU) in children and adolescents is associated with sleep disturbances, emotional difficulties, and poor academic performance. Early detection is challenging due to the multifactorial nature of the problem.

This project addresses PIU from a systems engineering perspective by designing and implementing:

- A predictive model to estimate PIU severity.
- A simulation scenario to analyze the evolution of the problem in a synthetic population.
- A web application that exposes the model through a REST API.

The data source used is the official Kaggle competition:

Child Mind Institute – Problematic Internet Use

---

## General Objective

To design and implement a system capable of predicting and analyzing the severity of problematic internet use in children and adolescents by integrating clinical data, psychological questionnaires, and biometric variables.

---

## Dataset and Target Variable

- Dataset: Child Mind Institute – Problematic Internet Use (Kaggle)
- Target variable: Severity Impairment Index (sii)
- Ordinal scale:
  - 0: No impairment
  - 1: Mild
  - 2: Moderate
  - 3: Severe
- Problem type: Semi-supervised ordinal classification
- Evaluation metric: Quadratic Weighted Kappa (QWK)

---

## System Architecture

The system follows a modular architecture based on the course workshops:

1. Data ingestion (CSV and Parquet files)
2. Data preprocessing and cleaning
3. Scenario 1 – Data-driven prediction (Machine Learning)
4. Scenario 2 – Event-driven simulation
5. Web application with REST API

---

## Scenario 1 – Predictive Model

- Model used: CatBoostClassifier
- Output type: Multiclass classification (sii 0–3)
- The model also supports a binary classification (normal / problematic).
- Relevant variables include PCIAT questionnaire scores, sleep scales, physical activity, and biometric features.

---

## Scenario 2 – Simulation

The second scenario implements an event-driven simulation using a cellular automaton.

- Each cell represents an individual.
- The state corresponds to the sii value.
- Transition rules consider individual state, internet use level, and neighbor influence.
- This scenario enables the analysis of system stability, sensitivity, and emergent patterns.

---

## Web Application

The project includes a web application that exposes the predictive model:

- Backend: Flask (REST API)
- Language: Python
- Features:
  - Upload of CSV and Parquet files
  - sii prediction
  - Binary risk classification
  - Probability estimates and confidence level
  - Download of results in CSV format

---

## Repository Structure

Systems_Analysis_and_Design/
- Catch_up/
- Workshops/
- Final_Course_Project/
  - FinalCourseProject/
  - The_final_version_of_the_paper.pdf
  - The_final_version_of_the_report.pdf
  - Final Poster - Team 20.pdf
  - Slides - Project Report.pdf
- README.md

All final project deliverables are located in the Final_Course_Project directory.

---

## Final Deliverables

This repository fulfills all requirements of the final course submission:

1. Final version of the paper (IEEE format – PDF)
2. Final version of the poster
3. Final version of the report
4. Presentation slides
5. GitHub repository with the complete project

---

## Team Members

- Bettsy Liliana Garcés Buriticá
- Marta Isabel Sánchez Caita
- Luis Fernando Rojas Rada

Universidad Distrital Francisco José de Caldas  
Course: Systems Analysis & Design

---

## References

- Child Mind Institute – Problematic Internet Use, Kaggle Competition
- Systems Analysis & Design course materials
