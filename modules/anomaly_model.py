import pandas as pd
from sklearn.ensemble import IsolationForest

def run_isolation_forest(df, contamination=0.02, random_state=42):
    """
    Applies Isolation Forest to the load profile data to detect anomalies.
    
    Parameters:
    - df: The Load_profile DataFrame (must contain 'UP - Block Load Energy KWH')
    - contamination: The proportion of outliers in the data
    
    Returns:
    - df: The DataFrame with an additional 'Is_Anomaly' column
    """
    # Initialize the model
    model = IsolationForest(contamination=contamination, random_state=random_state)
    
    # Fit the model (using the energy usage column)
    # Note: Ensure your column name matches your dataframe structure
    data_for_model = df[['UP - Block Load Energy KWH']] 
    
    # Predict (-1 is anomaly, 1 is normal)
    ai_scores = model.fit_predict(data_for_model)
    
    # Map to human-readable labels
    df['Is_Anomaly'] = ['Yes' if score == -1 else 'No' for score in ai_scores]
    
    return df