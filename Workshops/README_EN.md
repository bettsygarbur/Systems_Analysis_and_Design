# Workshop 1 - Systems Analysis & Design - Systems Engineering
## Child Mind Institute - Problematic Internet Use Competition

### How the Analysis Was Conducted

The analysis was conducted following the methodology established in the Workshop 1 requirements. The analysis was performed collaboratively by the work team.

**Applied Analysis Framework:**

**1. Competition Overview Analysis**
- Systematic review of the Child Mind Institute - Problematic Internet Use Kaggle competition
- Detailed examination of the Healthy Brain Network dataset structure (3,960 participants, 80+ attributes)
- Documentation of the Severity Impairment Index (SII) as target variable with 4 ordinal levels
- Analysis of the 30% missing data problem creating a semi-supervised learning challenge
- Evaluation of the Quadratic Weighted Kappa scoring metric with mathematical formulation: κ = 1 - (ΣW×O)/(ΣW×E)

**2. Systems Analysis Framework**
- Integration of heterogeneous physiological and behavioral signals from actigraphy and clinical assessments
- Mapping of system components: wrist accelerometer data (X, Y, Z, ENMO), fitness assessments, bioelectrical impedance analysis, and psychological questionnaires
- Identification of behavioral phenotypes through interaction analysis between physical activity patterns and internet usage
- Documentation of feedback loops between model performance signals and human adjudication for iterative improvement

**3. Complexity and Sensitivity Analysis**
- Assessment of high-dimensional, multimodal signal processing challenges
- Analysis of nonlinear interactions and context-dependent effects in behavioral systems
- Evaluation of system sensitivity to small perturbations (device artifacts, timing offsets, behavioral anomalies)
- Documentation of methodological mitigation strategies including temporally aware feature engineering and uncertainty-sensitive algorithms

**4. Chaos and Randomness Investigation**
- Analysis of chaotic dynamics in problematic internet use patterns
- Documentation of feedback loops: positive reinforcement (increased screen exposure → degraded sleep → more screen use)
- Examination of sensitivity to initial conditions in prediction tasks
- Conceptual modeling of behavioral phase spaces with multiple attractors (healthy engagement, risky use, problematic use)

### Code and Tools Used

**Document Preparation:**
- **LaTeX with IEEE Conference Format:** Used for academic report generation with proper mathematical notation
- **Overleaf Platform:** Online LaTeX editor for collaborative document preparation

**Analysis Tools:**
- **Systems Engineering Principles:** Application of course textbook methodologies
- **Mathematical Modeling:** Quadratic Weighted Kappa formulation and matrix operations (O, W, E matrices)
- **Theoretical Frameworks:** Chaos theory applications and complexity science principles

**Visualization Tool:**
- **draw.io:** Used for creating system architecture diagrams

**Data Source:**
- **Kaggle Competition Dataset:** Public dataset from Child Mind Institute's Healthy Brain Network study

### Repository Structure

Workshop_1/
├── README.md # This documentation file
└── workshop_1_final_report.pdf # Complete analysis report in IEEE format

### Team Composition

**Team Members:**
- **Bettsy Liliana Garces Buritica** (Code: 20231020222)
- **Marta Isabel Sanchez Caita** (Code: 20222020118)
- **Luis Fernando Rojas Rada** (Code: 20222020242)
- **[Team Member 4]** ()

**Course Information:**
- **Course:** Systems Analysis & Design
- **Institution:** Universidad Distrital Francisco José de Caldas
- **Instructor:** Eng. Carlos Andrés Sierra, M.Sc.
- **Semester:** 2025-III
- **Submission Date:** September 27, 2025

### Key Findings

**System Strengths:**
- Multimodal data integration combining objective sensor data with subjective clinical assessments
- High temporal resolution from continuous wrist actigraphy recordings
- Flexible modeling architecture supporting ordinal formulations and ensemble methods

**System Limitations:**
- 30% missing data in target variable creating semi-supervised learning challenges
- Extreme class imbalance (1.24% severe cases) affecting critical case detection
- Nonlinear system sensitivity amplifying small perturbations

### Competition Context and Scale

**Participation Metrics:**
- **Host:** Child Mind Institute (leading institution in child and adolescent mental health)
- **Prize Pool:** $60,000 in total prizes and medal points
- **Participation Scale:** 15,664 total entrants, 4,483 active participants organized into 3,559 teams
- **Submission Volume:** 84,049 total submissions demonstrating high engagement and iterative model development
- **Format:** Merger & Entry allowing team collaboration and knowledge sharing

**Competition Technical Details:**
- **Platform:** Kaggle
- **Duration:** September 19 - December 19, 2024
- **Dataset:** 3,960 participants with 80+ attributes
- **Target Variable:** SII with 4 ordinal levels (0: None, 1: Mild, 2: Moderate, 3: Severe)
- **Class Distribution:** 58.26% (Level 0), 26.28% (Level 1), 13.82% (Level 2), 1.24% (Level 3)
- **Evaluation Metric:** Quadratic Weighted Kappa
- **URL:** [https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use](https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use)

**Global Impact:** The substantial participation metrics (15,664 entrants, 84,049 submissions) reflect international recognition of problematic internet use as a critical public health challenge, with the competition serving as a catalyst for advancing predictive modeling methodologies in pediatric behavioral health assessment.

---

*This README documents the complete methodology, tools, and findings of our systems engineering analysis for Workshop 1.*
