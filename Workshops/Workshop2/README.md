# Workshop 2 - Systems Analysis & Design - Systems Engineering
## Child Mind Institute - Problematic Internet Use Competition

## Overview  
This project presents a predictive system designed to identify potential patterns of Problematic Internet Use (PIU) in children and adolescents.  
The system integrates physical activity and behavioral data to train an AI-based model capable of estimating the risk of internet addiction from user responses and quantitative indicators derived from clinical and accelerometer data.  

The work aligns with the objectives of the Child Mind Institute’s Healthy Brain Network, aiming to promote early detection of behavioral disorders through computational tools and AI-assisted assessment.

## System Architecture  

The system is organized into three main components:

## 1. Frontend / User Interface
- Provides an interactive form for users to complete a PIU evaluation questionnaire.  
- Displays the results and personalized feedback through a result panel.  
- Ensures accessibility and usability through a web interface.  

## 2. Backend
- Manages the reception, integration, and communication of user data.  
- Calls the predictive model API that processes the information from the frontend.  
- Guarantees secure communication and synchronization between modules.  

## 3. Data Processing Layer
- Handles data ingestion, cleaning, and normalization.  
- Implements feature engineering, model training, validation, and evaluation.  
- Combines quantitative and qualitative data for model predictions.  
- Integrates with MySQL databases and cloud storage for clinical and accelerometer information.  

#### Diagram 1: General System Flow (Client – Frontend – Backend)
![Diagram 1](bfee3b87-0403-4869-891d-682f94fdec4a.png)

#### Diagram 2: Data and Processing Architecture
![Diagram 2](de8a4ef6-614e-41c2-91cf-4a0572361939.png)

---

## Development Process  

The development followed a structured and iterative methodology, which included:
1. Designing the data flow between the frontend interface and backend prediction services.  
2. Defining preprocessing pipelines for normalization and feature extraction.  
3. Training and validating predictive models using competition-aligned datasets.  
4. Integrating predictive outputs into a dashboard for user interpretation.  

This approach ensures that the system remains adaptable to new datasets or modeling techniques while maintaining consistency and interpretability.

---

## AI Predictive Model  
The predictive model applies supervised learning methods to analyze both quantitative metrics (accelerometer data, clinical records) and qualitative inputs (survey responses).  
It generates a prediction of the user's potential risk level for Problematic Internet Use.  
The model operates through an API service integrated into the backend, allowing automated interaction between components.

---

## Sensitivity and Reliability  
To address data variability and maintain stable predictions:
- Data normalization and cleaning procedures were implemented to manage missing or inconsistent information.  
- The backend includes error-handling routines for unexpected inputs or connection issues.  
- Continuous evaluation mechanisms are proposed to ensure reliability and model robustness.  

---

## Documentation  
This `README.md` outlines the project’s structure, the system’s development process, and references the corresponding architectural diagrams.  
The repository also contains the complete project report in PDF format, which includes theoretical foundations, data sources, and validation results.

[Link to final PDF report](./Final_Paper.pdf)

**Team Members:**
- **Bettsy Liliana Garces Buritica** (Code: 20231020222)
- **Marta Isabel Sanchez Caita** (Code: 20222020118)
- **Luis Fernando Rojas Rada** (Code: 20222020242)
- **Mauricio Daniel Baes Sánchez** (Code: 20222020058)

**Course Information:**
- **Course:** Systems Analysis & Design
- **Institution:** Universidad Distrital Francisco José de Caldas
- **Instructor:** Eng. Carlos Andrés Sierra, M.Sc.
- **Semester:** 2025-III
- **Submission Date:** October 18, 2025
