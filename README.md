================================================================================
PROJECT      : Advanced Analytics for Smart Grid Revenue Protection
ORGANIZATION : Larsen & Toubro (L&T) Construction
AUTHOR       : Pranjal
MENTOR/GUIDE : Mr. Omkar Verma
DATE         : June 2026
================================================================================

1. PROJECT OVERVIEW
-------------------
This repository contains an end-to-end, fully automated Machine Learning and 
Data Engineering pipeline designed for Advanced Metering Infrastructure (AMI). 
The architecture ingests raw EAV (Entity-Attribute-Value) telemetry, normalizes 
timestamps, flags high-variance statistical anomalies, performs a physics-based 
revenue protection audit, and utilizes a Random Forest Regressor to forecast 
feeder-level substation demand.

2. SYSTEM ARCHITECTURE (THE 4 MODELS)
-------------------------------------
The assembly line is decoupled into four distinct engines:
- Model 1 (Ingestion & ETL) : Transforms raw EAV data into a Wide-Spine EAV matrix, 
                              handling forward-fill imputation and time-series extraction.
- Model 2 (AI Diagnostics)  : Unsupervised Scikit-Learn Isolation Forest (2.0% 
                              contamination) to detect macro-variance consumption spikes.
- Model 3 (Revenue Audit)   : A deterministic truth-table cross-referencing active 
                              power (V x I) against internal microcontroller Bitwise 
                              hardware diagnostic registers (Codes 0, 32, 128, 160).
- Model 4 (Load Forecaster) : Supervised Random Forest Regressor aggregated at the 
                              Feeder/Substation level to predict diurnal demand rhythms.

3. REPOSITORY STRUCTURE
-----------------------
/Smart_Meter_Synchronisation_Project
│
├── /data
│   ├── Daily_Billing_Load Profile.xlsx       <- Raw Input Telemetry
│   ├── Master_Enriched_Grid_Telemetry.csv    <- Pipeline Output 1 (Cleaned Spine)
│   ├── Grid_Demand_Forecast_Horizon.csv      <- Pipeline Output 2 (AI Predictions)
│   └── Figure_4.4_Declustered_Forecast.png   <- Rendered Matplotlib Output
│
├── /modules
│   ├── __init__.py
│   ├── data_processor.py       (Executes Model 1)
│   ├── anomaly_model.py        (Executes Model 2)
│   ├── theft_detector.py       (Executes Model 3)
│   └── forecaster.py           (Executes Model 4)
│
├── /notebooks
│   └── analysis.ipynb          (Interactive Executive Storyboard)
│
└── main_pipeline.py            (Master Execution Orchestrator)


4. INSTALLATION & ENVIRONMENT REQUIREMENTS
----------------------------------------
Ensure Python 3.9+ is installed. The following enterprise libraries are required:
> pip install pandas numpy scikit-learn matplotlib seaborn openpyxl

5. EXECUTION INSTRUCTIONS
-------------------------
Step 1: The Factory Pipeline (Backend)
Open your terminal, navigate to the root directory, and execute the master orchestrator:
> cd Smart_Meter_Synchronisation_Project
> python main_pipeline.py

This will ingest the raw Excel file, process 66,000+ ticks, output the ASCII 
Audit Table to the console, and serialize the enriched CSV files to the /data folder.

Step 2: The Executive Storyboard (Frontend)
Once the pipeline successfully executes, open `/notebooks/analysis.ipynb`.
Run the cells sequentially to load the enriched data, calculate total INR (Rupee) 
fiscal leakage, and render the high-resolution 300-DPI Substation Forecasting plots.

================================================================================
Confidentiality Note: This codebase contains proprietary diagnostic logic developed 
under L&T Construction guidelines.
================================================================================