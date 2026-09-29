import pandas as pd
import numpy as np

def detect_energy_theft(df):
    """
    Model 3: Advanced Multi-Factor Revenue Protection Engine.
    Evaluates physical electrical load against microcontroller diagnostic error registers.
    """
    print("-> [Stage 5] Executing Multi-Factor Theft, Bypass & Hardware Fault classification...")
    
    # Standardize health indicator column to integers to prevent type mismatch
    df['UP - Meter Health Indicator'] = df['UP - Meter Health Indicator'].fillna(0).astype(int)
    
    # Initialize baseline state
    df['Grid_Diagnostic_State'] = 'Normal Consumption'
    
    # Condition 1: Pure Grid Outage or Downstream Disconnect (V < 50V)
    outage = (df['UP - Block Load Energy KWH'] <= 0.01) & (df['UP - Average Voltage'] < 50.0)
    df.loc[outage, 'Grid_Diagnostic_State'] = 'Grid Outage / Total Disconnect'
    
    # Condition 2: Parasitic Phantom Load (TVs, WiFi routers drawing < 75 Watts on standby)
    phantom = (
        (df['UP - Block Load Energy KWH'] <= 0.01) & 
        (df['UP - Average Voltage'] > 200.0) & 
        (df['UP - Average Current'] <= 0.4) &
        (df['UP - Meter Health Indicator'] == 0)
    )
    df.loc[phantom, 'Grid_Diagnostic_State'] = 'Normal Standby (Phantom Load)'
    
    # Condition 3: Physical Hardware Tampering / Battery Warning (Code 32)
    fault_32 = (df['UP - Meter Health Indicator'] == 32)
    df.loc[fault_32, 'Grid_Diagnostic_State'] = 'Technical Fault: Terminal Cover Open / Battery Low'

    # Condition 4: High-Risk Magnetic Shunt Tampering / Sync Loss (Code 128 or composite 160)
    tamper_128 = df['UP - Meter Health Indicator'].isin([128, 160])
    df.loc[tamper_128, 'Grid_Diagnostic_State'] = 'Critical Alarm: Magnetic Saturation Tampering'

    # Condition 5: Confirmed Physical Line Bypass (The "Holy Grail" Theft catch)
    # Meter claims it is perfectly healthy (Code 0), but heavy current is bypassing the sensor!
    true_bypass = (
        (df['UP - Block Load Energy KWH'] <= 0.01) & 
        (df['UP - Average Voltage'] > 200.0) & 
        (df['UP - Average Current'] > 0.4) &
        (df['UP - Meter Health Indicator'] == 0)
    )
    df.loc[true_bypass, 'Grid_Diagnostic_State'] = 'Confirmed Theft: Unmetered Physical Line Bypass'

    return df