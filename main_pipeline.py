"""
================================================================================
PROJECT      : Advanced Analytics for Smart Grid Revenue Protection
ORGANIZATION : Larsen & Toubro (L&T)
MENTOR/GUIDE : Mr. Omkar Verma
AUTHOR       : Pranjal
FILE         : main_pipeline.py (Definitive Master Orchestrator - All 4 Models)
================================================================================
Description:
Executes the fully synchronized, end-to-end AMI Telemetry assembly line:
  - Model 1 : Master Ingestion, Datetime Normalization & Long-to-Wide Pivoting
  - Model 2 : AI Unsupervised Outlier Classification (Isolation Forest 2.0%)
  - Model 3 : Multi-Factor Revenue Protection Audit (Live Physics + Bitwise Registers)
  - Model 4 : Supervised Time-Series Demand Forecaster (Random Forest Regressor)
================================================================================
"""

import os
import sys
import pandas as pd
import numpy as np

# Elite feature: Force Python to recognize the local workspace regardless of execution directory
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from modules.data_processor import load_and_clean_data
from modules.anomaly_model import run_isolation_forest
from modules.theft_detector import detect_energy_theft
from modules.forecaster import train_and_forecast_load

# Define immutable relative system paths for robust execution
DATA_INPUT_PATH = os.path.join("data", "Daily_Billing_Load Profile.xlsx")
EXPORT_ENRICHED_PATH = os.path.join("data", "Master_Enriched_Grid_Telemetry.csv")
EXPORT_FORECAST_PATH = os.path.join("data", "Grid_Demand_Forecast_Horizon.csv")


def print_banner():
    print("\n" + "="*80)
    print("    LARSEN & TOUBRO CONSTRUCTION - SMART GRID AMI MASTER ORCHESTRATOR")
    print("="*80 + "\n")


def print_section(title):
    print(f"\n[>>>] {title.upper()}")
    print("-" * (len(title) + 6))


def main():
    print_banner()
    
    # -------------------------------------------------------------------------
    # STAGES 1 to 4: MASTER NORMALIZATION & EAV PIVOTING (Model 1)
    # -------------------------------------------------------------------------
    print_section("Stages 1-4: Telemetry Normalization & Wide-Spine Generation")
    
    if not os.path.exists(DATA_INPUT_PATH):
        print(f"\n[CRITICAL HALT] Raw dataset not located at expected path: '{DATA_INPUT_PATH}'")
        print("-> Action: Verify that 'Daily_Billing_Load Profile.xlsx' sits inside the '/data' subdirectory.")
        sys.exit(1)

    try:
        daily_df, billing_df, load_cleaned = load_and_clean_data(DATA_INPUT_PATH)
    except Exception as e:
        print(f"\n[FATAL EXCEPTION] Pipeline failed during Stage 1-4 execution: {str(e)}")
        sys.exit(1)

    total_records = len(load_cleaned)
    print(f"[*] Wide-Format Spine assembled cleanly. Total Telemetry Ticks: {total_records:,}")

    # -------------------------------------------------------------------------
    # STAGE 5: AI UNSUPERVISED ANOMALY DIAGNOSTICS (Model 2)
    # -------------------------------------------------------------------------
    print_section("Stage 5: AI Anomaly Diagnostics (Isolation Forest Contamination: 2.0%)")
    
    load_with_anomalies = run_isolation_forest(load_cleaned)
    
    anomaly_counts = load_with_anomalies['Is_Anomaly'].value_counts()
    anom_count = anomaly_counts.get('Yes', 0)
    anom_rate = (anom_count / total_records) * 100
    
    print(f"[*] High-Variance Outliers detected : {anom_count:>6,} ({anom_rate:.2f}% of total grid load)")
    print(f"[*] Baseline Standard Ticks       : {anomaly_counts.get('No', 0):>6,}")

    # -------------------------------------------------------------------------
    # STAGE 6: MULTI-FACTOR REVENUE PROTECTION AUDIT (Model 3)
    # -------------------------------------------------------------------------
    print_section("Stage 6: Multi-Factor Revenue Protection Audit (Physics + Bitwise logic)")
    
    master_grid = detect_energy_theft(load_with_anomalies)
    audit_summary = master_grid['Grid_Diagnostic_State'].value_counts()
    
    # Generate the high-polish ASCII Table for your MS Word Report screenshot
    print("\n" + "."*75)
    print("   OFFICIAL L&T REVENUE PROTECTION GRID COMPLIANCE AUDIT")
    print("."*75)
    for category, count in audit_summary.items():
        pct = (count / total_records) * 100
        print(f"  {category:<52} : {count:>7,}  ({pct:>5.1f}%)")
    print("."*75)

    # Compute financial exposure logic specifically for L&T management
    theft_ticks = audit_summary.get('Confirmed Theft: Unmetered Physical Line Bypass', 0)
    mag_ticks = audit_summary.get('Critical Alarm: Magnetic Saturation Tampering', 0)
    total_leakage_ticks = theft_ticks + mag_ticks

    if total_leakage_ticks > 0:
        print(f"\n[!] DISPATCH PRIORITY: {total_leakage_ticks:,} unmetered grid intervals demand field inspection.")
    else:
        print("\n[V] GRID SECURE: 0 confirmed incidents of active power bypass detected.")

    # -------------------------------------------------------------------------
    # STAGE 7: DATA SERIALIZATION
    # -------------------------------------------------------------------------
    print_section("Stage 7: Enriched Data Serialization")
    
    os.makedirs(os.path.dirname(EXPORT_ENRICHED_PATH), exist_ok=True)
    master_grid.to_csv(EXPORT_ENRICHED_PATH, index=False)
    
    print(f"[*] Canonical Enriched Dataframe written to : {EXPORT_ENRICHED_PATH}")
    print(f"[*] Enriched Matrix dimensions              : {master_grid.shape}")

    # -------------------------------------------------------------------------
    # STAGE 8: SUPERVISED AI LOAD FORECASTING (Model 4)
    # -------------------------------------------------------------------------
    print_section("Stage 8: Supervised AI Demand Forecaster (Random Forest Regressor)")
    
    # Execute Model 4 using the pristine data filter
    rf_engine, forecast_table, precision_scores = train_and_forecast_load(master_grid)
    
    # Output Enterprise Precision Metrics
    print("\n" + "-"*50)
    print("      AI FORECASTER PRECISION DIAGNOSTIC")
    print("-"*50)
    print(f"  Mean Absolute Error (MAE)  : {precision_scores['MAE']:>7.4f} kWh")
    print(f"  Root Mean Squared (RMSE)   : {precision_scores['RMSE']:>7.4f} kWh")
    print(f"  Mathematical R2 Confidence : {precision_scores['R2']*100:>6.1f} %")
    print("-"*50)

    # Save the forecasted delivery horizon
    forecast_table.to_csv(EXPORT_FORECAST_PATH, index=False)
    print(f"[*] Forecasted Demand Horizon saved to      : {EXPORT_FORECAST_PATH}")
    print(f"[*] Forecast Matrix dimensions              : {forecast_table.shape}")

    print("\n" + "="*80)
    print(" [FLAGSHIP DELIVERY COMPLETE] ALL 4 L&T MODELS SYNCHRONIZED AND SECURED.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()