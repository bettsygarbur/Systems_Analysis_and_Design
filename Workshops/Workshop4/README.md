# 📘 README — Workshop 4: Simulation of Complex Systems for *Problematic Internet Use*

This repository contains the work completed for **Workshop 4**, focused on designing and executing two simulation scenarios using the Kaggle dataset **Child Mind Institute – Problematic Internet Use**.  
The project connects the system architecture developed in Workshops 1–3 (ingestion, preprocessing, modular design) with the simulation and complexity analysis carried out here.

> **Simulation Report (PDF):**  
> 👉[Simulation Report (PDF)](Simulation_Report.pdf)


---


## 🧩 Overview of the Topics Covered

### **1. Data Preparation**
- Integration of dataset files (train/test/data dictionary).  
- Grouping of variables by instrument (Demographics, PCIAT, Sleep, Physical, etc.).  
- Management of the **semi-supervised** nature of the dataset.  
- Construction of the *sii* target using *PCIAT Total* thresholds.  
- Missing data handling, feature filtering, winsorization, scaling.  
- Extraction and aggregation of **actigraphy time-series** features.

### **2. Simulation Planning**
Two complementary scenarios were designed:

#### **Scenario 1: Data-Driven (Machine Learning Pipeline)**
- Feature subsets (tabular-only, tabular + PCIAT, sleep variables, etc.).  
- CatBoost classifier with class weighting and categorical handling.  
- Evaluation via **Quadratic Weighted Kappa (QWK)**.  
- Sensitivity analysis: hyperparameters, missing values, perturbations.

#### **Scenario 2: Event-Based (Cellular Automaton)**
- Population mapped onto a 2D grid.  
- States representing *sii* levels (0–3) and discretized attributes.  
- Moore neighborhood, stochastic components, rule variations.  
- Observation of clusters, propagation waves, absorbing states.

### **3. Running the Simulations**
- Multiple ML configurations trained and compared.  
- Behavior observed for classes 2–3 (instability, class imbalance).  
- CA simulations run with varied weights, thresholds, and noise.  
- Recording of global state distributions and spatial patterns.

### **4. Code Structure & Implementation Highlights**
- Clean separation of ingestion, preprocessing, modeling, and simulation.  
- Explicit normalization of categorical features for CatBoost.  
- Balanced class weights applied for imbalanced targets.  
- Cellular automaton based on synchronized updates and probabilistic rules.

### **5. Results & Discussion**
- QWK in the *fair-to-moderate* range across experiments.  
- ML pipeline showed sensitivity to data quality and feature choices.  
- Automata produced cluster formation and occasional unrealistic dynamics.  
- Proposal for a hybrid ML–CA framework for improved calibration and robustness.

---

## 🖼️ Figures Included

- **`salida1.jpg`** — Sample output from Scenario 1 (ML).  
- **`salida2.jpg`** — Sample output from Scenario 2 (Cellular Automaton).

---

## 🧪 How to Reproduce

1. Place `train.csv`, `test.csv`, and other inputs inside `/data/`.  
2. Run the scripts:

```bash
python doct.py
python scenario2.py
