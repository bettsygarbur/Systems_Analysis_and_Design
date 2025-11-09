# Workshop 3 - Problematic Internet Use Prediction


## Reviewing and Refining of System Architecture

### Identified Positives on the System
The system is well thought out, with a clear modular architecture (frontend, backend, data processing, infrastructure) that enhances maintainability and scalability. It aligns with systems engineering principles emphasizing resilience, validation, and security. It manages heterogeneous data (CSV and Parquet), applies robust imputation for missing values, and uses ordinal regression with Quadratic Weighted Kappa. Priority is given to user experience via a responsive interface, interpretability of predictions, and report downloads. Sensitivity to chaotic human behavior is acknowledged with preprocessing, recalibration, and monitoring.

### Possibly Problematic Points of Design
Challenges include reliance on pre-trained models (e.g., GPT) potentially unsuited for ordinal regression, bias risks due to missing severity labels, performance bottlenecks when integrating large actigraphy time series under tight time constraints, and lightly addressed security concerns for clinical data. Detailed planning for data pipelines, model lifecycle, and privacy compliance is needed for production readiness.

### Plans for Refining
1. **Scalability**: Microservices, container orchestration (Docker, Kubernetes), streaming data ingestion  
2. **Fault Tolerance**: Redundancy, circuit breakers, monitoring tools (Prometheus, Grafana)  
3. **Strategic**: MLOps lifecycle, privacy and compliance (HIPAA, GDPR)

## Quality and Risk Analysis

### Potential Risks and Mitigations
- **Frontend:** Incompatible file uploads — enforce validation and restrict file types (OWASP guidance)  
- **Backend:** Endpoint failure — load balancing, alerts, exception handling (ISO 27005)  
- **Storage:** DB-cloud sync inconsistencies — periodic integrity checks (NIST RMF)  
- **Model:** Predictive bias — data audits, balancing, review (CRISP-DM)  
- **Security:** Unauthorized access — access controls, encryption, audit logs (ISO 27001 / NIST SP 800-53)  

Continuous monitoring and incident management are established to ensure stability and support corrective workflows for continuous improvement.

## Project Management Plan

### Roles and Responsibilities
- **Data Analyst & Model Developer:** Data preparation, feature engineering, model design and validation  
- **Backend Developer:** Backend logic, API development, model-DB-UI integration  
- **UI/UX Developer:** Responsive interfaces, dashboards, visualization  
- **Coordinator & Documenter:** Workflow continuity, quality control, documentation, versioning  

### Milestones and Deliverables
1. Data understanding, requirement specifications, repo setup  
2. Data preprocessing, feature engineering  
3. Model development and training, validation  
4. Backend and UI integration  
5. Validation, optimization, and testing  
6. Final deployment and documentation  

### Methodology and Tools
Hybrid Scrum-Kanban framework with weekly sprints, reviews, and task boards. Tools include GitHub (code \& documentation), Google Drive/Notion (planning), VSCode (development), MySQL Workbench (DB management), and Slack/Discord (communication).

### Workflow Diagram
See the attached `workflowDiagram.png` for the project workflow.

## Incremental Improvements

### Evolution from Workshop 1 to Workshop 3
Across three phases, the system progressed from conceptual system analysis for a multimodal dataset (including actigraphy, physical fitness, bioimpedance, psychometrics) with semi-supervised handling of ~30% missing labels in SII, through architecture design emphasizing modularity and specialized technology stack (Python backend, JS frontend, MySQL DB), to feature filtering and model refinement with stratified validation and threshold optimization.

### Preprocessing and Quality Assurance
Filtering reduced variables to 69 numerical and 7 categorical features. Quality assurance evolved to continuous monitoring, imputation strategies, sensitivity analysis, version control, and reproducible deployment workflows.

## Documentation and Delivery

### Comprehensive Deliverables Structure
Documentation aligned with Workshop 3 guidelines integrating preprocessing, modeling, validation, and risk mitigation artifacts, with clear traceability and citation to standards.

### Core Documentation Components
Preprocessing functions, automated feature extraction for actigraphy, hyperparameter tuning (XGBoost, LightGBM, CatBoost), unit tests, processed datasets, performance matrices, and final predictions.

### Architecture and Risk Analysis
Designed to satisfy robust design principles and aligned with ISO 9001:2015 and CMMI Level 2. Risk analysis and mitigation include data quality, availability, security, and privacy considerations.

### Project Coordination and Validation
Defined roles and milestone alignment, with emphasis on documentation, peer reviews, sprint tracking, and validation metrics (QWK), reporting moderate reliability in dealing with imbalanced ordinal classifications.

---

## References

- Child Mind Institute. Child Mind Institute — Problematic Internet Use, *Kaggle Competition Platform*, 2024. Available: https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use

- RM503. CMI-Problematic_Internet_Usage, GitHub repository, 2024. Available: https://github.com/RM503/CMI-Problematic_Internet_Usage

## Team Members
- Bettsy Liliana Garcés Buriticá (code: 20231020222, blgarcesb@udistrital.edu.co)  
- Marta Isabel Sánchez Caita (code: 20222020118, maisanchezc@udistrital.edu.co)  
- Luis Fernando Rojas Rada (code: 20222020242, lfrojasr@udistrital.edu.co)  
- Mauricio Daniel Baes Sánchez (code: 20222020058, mdbaess@udistrital.edu.co)
[Link to Workshop 3](./Workshop_3-Team_20.pdf)
