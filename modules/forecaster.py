import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_and_forecast_load(df):
    """
    Model 4: Enterprise Feeder-Level Demand Forecaster.
    Filters out theft/blackouts, aggregates individual smart meters into a unified 
    Substation Grid curve, and trains a Random Forest Regressor.
    """
    print("-> [Stage 8] Aggregating AMI ticks into unified Feeder Substation load...")
    
    # 1. Isolate strictly honest, active grid consumption
    df['READ_DTTM'] = pd.to_datetime(df['READ_DTTM'])
    pristine_grid = df[df['Grid_Diagnostic_State'] == 'Normal Consumption'].copy()
    
    if len(pristine_grid) == 0:
        print("   [!] Fallback: No 'Normal Consumption' tag found. Using raw load...")
        pristine_grid = df.copy()

    # --- THE SENIOR ENGINEERING FIX: AGGREGATE TO FEEDER LEVEL ---
    # Sum the KWH of all individual meters operating at that exact second
    substation_curve = pristine_grid.groupby(
        ['READ_DTTM', 'Hour', 'DayOfWeek', 'Month', 'Is_Weekend']
    )['UP - Block Load Energy KWH'].sum().reset_index()

    substation_curve = substation_curve.rename(columns={'UP - Block Load Energy KWH': 'Substation_Demand_KWH'})
    substation_curve = substation_curve.sort_values('READ_DTTM').reset_index(drop=True)

    # 2. Define Time-Series Spine
    features = ['Hour', 'DayOfWeek', 'Month', 'Is_Weekend']
    target = 'Substation_Demand_KWH'

    X = substation_curve[features]
    y = substation_curve[target]

    # 3. Chronological 80/20 Time-Series Split
    split_idx = int(len(substation_curve) * 0.8)
    
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    print(f"   - Aggregated Feeder Ticks : {len(substation_curve):,} consolidated hourly intervals")
    print(f"   - Substation Train Window : {len(X_train):,} historical ticks")
    print(f"   - Substation Test Horizon : {len(X_test):,} unseen future ticks")

    # 4. Train the tuned Regressor
    rf_engine = RandomForestRegressor(n_estimators=150, max_depth=10, random_state=42)
    rf_engine.fit(X_train, y_train)

    # 5. Predict the Substation Horizon
    y_pred = rf_engine.predict(X_test)

    # 6. Capture Enterprise Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    # Format the delivery export table cleanly
    delivery_table = substation_curve.iloc[split_idx:].copy()
    delivery_table['AI_Forecasted_Demand_KWH'] = y_pred
    delivery_table['Dispatch_Error_KWH'] = np.abs(delivery_table['Substation_Demand_KWH'] - y_pred)

    metrics = {'MAE': mae, 'RMSE': rmse, 'R2': r2}

    return rf_engine, delivery_table, metrics