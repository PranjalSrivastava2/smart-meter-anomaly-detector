import pandas as pd
import numpy as np

def load_and_clean_data(file_path):
    """
    Master Ingestion and Preprocessing Engine for Smart Grid AMI Telemetry.
    Ingests raw long-format telemetry, normalizes datetimes, pivots to wide format,
    standardizes column headers, imputes missing telemetry, and extracts time-series features.
    """
    print("-> [Stage 1] Ingesting raw AMI sheets...")
    daily_df = pd.read_excel(file_path, sheet_name="Daily_profile")
    billing_df = pd.read_excel(file_path, sheet_name="Billing_profile")
    load_raw_df = pd.read_excel(file_path, sheet_name="Load_profile")

    print("-> [Stage 2] Normalizing timestamps to high-precision datetimes...")
    load_raw_df['READ_DTTM'] = pd.to_datetime(load_raw_df['READ_DTTM'], dayfirst=True, errors='coerce')
    daily_df['READ_DTTM'] = pd.to_datetime(daily_df['READ_DTTM'], dayfirst=True, errors='coerce')
    
    billing_dates = ['START_DTTM', 'END_DTTM', 'CRE_DTTM', 'STATUS_UPD_DTTM']
    for col in billing_dates:
        if col in billing_df.columns:
            billing_df[col] = pd.to_datetime(billing_df[col], format='mixed', dayfirst=True, errors='coerce')

    print("-> [Stage 3] Pivoting Load Profile from Long to Wide telemetry format...")
    load_raw_df['MEASUREMENT_TYPE_NAME'] = load_raw_df['MEASUREMENT_TYPE_NAME'].astype(str).str.strip()
    
    load_wide_df = load_raw_df.pivot_table(
        index=['METER_NUMBER', 'READ_DTTM'],
        columns='MEASUREMENT_TYPE_NAME',
        values='READS',
        aggfunc='first'
    ).reset_index()

    load_wide_df = load_wide_df.sort_values(by=['METER_NUMBER', 'READ_DTTM']).reset_index(drop=True)

    print("-> [Stage 4] Standardizing headers and executing safe imputation...")
    rename_map = {}
    for col in load_wide_df.columns:
        col_str = str(col).strip()
        if 'Energy KWH' in col_str or 'Block Load' in col_str:
            rename_map[col] = 'UP - Block Load Energy KWH'
        elif 'Voltage' in col_str:
            rename_map[col] = 'UP - Average Voltage'
        elif 'Current' in col_str:
            rename_map[col] = 'UP - Average Current'
        elif 'Signal' in col_str:
            rename_map[col] = 'UP - Average Signal Strength'
            
    load_wide_df.rename(columns=rename_map, inplace=True)

    # SAFEGUARD 1: Strictly drop any accidentally duplicated column headers
    load_wide_df = load_wide_df.loc[:, ~load_wide_df.columns.duplicated()].copy()

    core_telemetry_cols = [
        'UP - Block Load Energy KWH',
        'UP - Average Voltage',
        'UP - Average Current',
        'UP - Average Signal Strength'
    ]
    
    for col in core_telemetry_cols:
        if col not in load_wide_df.columns:
            default_val = 250.0 if 'Voltage' in col else 0.0
            load_wide_df[col] = default_val

    # SAFEGUARD 2: Perform imputation safely column-by-column
    for col in core_telemetry_cols:
        load_wide_df[col] = load_wide_df[col].ffill().fillna(0.0)

    # Generate Temporal Features required for AI Load Forecasting
    load_wide_df['Hour'] = load_wide_df['READ_DTTM'].dt.hour
    load_wide_df['DayOfWeek'] = load_wide_df['READ_DTTM'].dt.dayofweek
    load_wide_df['Month'] = load_wide_df['READ_DTTM'].dt.month
    load_wide_df['Is_Weekend'] = load_wide_df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)

    print("-> Data normalization and pivoting successfully completed!")
    return daily_df, billing_df, load_wide_df