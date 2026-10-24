"""
src/preprocessing.py
Data Preprocessing and Feature Engineering Module for Healthcare Facility Analytics.

This module loads the raw California HCAI Hospital Quarterly Financial & Utilization
dataset, validates the schema, handles missing/invalid values, engineers standardized
operational and financial performance metrics, and scales the feature matrix.
"""

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler


CORE_IDENTIFIER_COLS = [
    'FAC_NO', 'FAC_NAME', 'YEAR_QTR', 'COUNTY_NAME', 'TYPE_CNTRL', 'TYPE_HOSP', 'OP_STATUS'
]

REQUIRED_RAW_METRIC_COLS = [
    'LIC_BEDS', 'AVL_BEDS', 'STF_BEDS', 'DIS_TOT', 'DAY_TOT', 'VIS_TOT',
    'NET_TOT', 'OTH_OP_REV', 'TOT_OP_EXP'
]

FEATURE_NAMES = [
    'OP_MARGIN',
    'EXP_REV_RATIO',
    'REV_PER_BED',
    'EXP_PER_BED',
    'OCCUPANCY_RATE',
    'STF_AVL_RATIO',
    'ALOS',
    'OUTPATIENT_RATIO'
]

FEATURE_DESCRIPTIONS = {
    'OP_MARGIN': 'Operating Margin: (Total Operating Revenue - Operating Expenses) / Total Operating Revenue',
    'EXP_REV_RATIO': 'Expense-to-Revenue Ratio: Total Operating Expenses / Total Operating Revenue',
    'REV_PER_BED': 'Operating Revenue per Available Bed ($ per bed)',
    'EXP_PER_BED': 'Operating Expenses per Available Bed ($ per bed)',
    'OCCUPANCY_RATE': 'Bed Occupancy Rate: Total Patient Days / (Available Beds * Total Days in Period)',
    'STF_AVL_RATIO': 'Staffed-to-Available Beds Ratio: Staffed Beds / Available Beds',
    'ALOS': 'Average Length of Stay: Total Inpatient Days / Total Discharges (Days)',
    'OUTPATIENT_RATIO': 'Outpatient Intensity: Total Outpatient Visits / Total Inpatient Days'
}


def load_raw_dataset(raw_csv_path: str = os.path.join("data", "raw", "combined_quarterly_raw.csv")) -> pd.DataFrame:
    """
    Loads and validates the combined quarterly raw dataset.
    """
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw data file not found at: {raw_csv_path}. Please run data fetch script first.")
    
    df = pd.read_csv(raw_csv_path, low_memory=False)
    df.columns = [str(c).strip().upper() for c in df.columns]
    
    # Schema validation
    missing_cols = [c for c in REQUIRED_RAW_METRIC_COLS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Schema validation error: Missing required raw columns: {missing_cols}")
    
    return df


def clean_quarterly_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Cleans raw quarterly observations, filtering closed facilities and non-operational records.
    Returns cleaned dataframe and audit exclusion statistics.
    """
    total_raw = len(df)
    
    # 1. Operational status
    open_mask = (df['OP_STATUS'].str.strip().str.upper() == 'OPEN') if 'OP_STATUS' in df.columns else pd.Series(True, index=df.index)
    closed_count = int((~open_mask).sum())
    
    # 2. Positive beds, discharges, days, expenses, and revenues
    df_clean = df[open_mask].copy()
    
    # Safe numeric coercion
    for col in REQUIRED_RAW_METRIC_COLS:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
    
    valid_capacity = (df_clean['AVL_BEDS'] > 0)
    valid_util = (df_clean['DIS_TOT'] > 0) & (df_clean['DAY_TOT'] > 0)
    df_clean['TOT_OP_REV'] = df_clean['NET_TOT'] + df_clean['OTH_OP_REV']
    valid_fin = (df_clean['TOT_OP_EXP'] > 0) & (df_clean['TOT_OP_REV'] > 0)
    
    valid_mask = valid_capacity & valid_util & valid_fin
    excluded_records = int((~valid_mask).sum())
    
    df_clean = df_clean[valid_mask].copy()
    
    audit_log = {
        'total_raw_records': total_raw,
        'closed_facilities_excluded': closed_count,
        'zero_capacity_or_utilization_excluded': excluded_records,
        'clean_quarterly_records': len(df_clean),
        'unique_clean_facilities': df_clean['FAC_NO'].nunique() if 'FAC_NO' in df_clean.columns else 0
    }
    
    return df_clean, audit_log


def build_facility_annual_profiles(df_clean: pd.DataFrame, target_year: int = 2023) -> pd.DataFrame:
    """
    Aggregates quarterly records into annualized facility-level profiles for a complete calendar year.
    Only facilities reporting all 4 quarters of the target year are retained to eliminate seasonal bias.
    """
    qtrs = [int(f"{target_year}{q}") for q in [1, 2, 3, 4]]
    df_year = df_clean[df_clean['YEAR_QTR'].isin(qtrs)].copy()
    
    agg_funcs = {
        'FAC_NAME': 'first',
        'COUNTY_NAME': 'first',
        'TYPE_CNTRL': 'first',
        'TYPE_HOSP': 'first',
        'YEAR_QTR': 'count',
        'LIC_BEDS': 'mean',
        'AVL_BEDS': 'mean',
        'STF_BEDS': 'mean',
        'DIS_TOT': 'sum',
        'DAY_TOT': 'sum',
        'VIS_TOT': 'sum',
        'TOT_OP_REV': 'sum',
        'TOT_OP_EXP': 'sum'
    }
    
    # Filter only available columns
    actual_agg = {k: v for k, v in agg_funcs.items() if k in df_year.columns}
    
    fac_df = df_year.groupby('FAC_NO').agg(actual_agg).reset_index()
    fac_df.rename(columns={'YEAR_QTR': 'QUARTERS_REPORTED'}, inplace=True)
    
    # Keep facilities reporting all 4 quarters with positive operational measures
    fac_df = fac_df[
        (fac_df['QUARTERS_REPORTED'] == 4) &
        (fac_df['AVL_BEDS'] > 0) &
        (fac_df['TOT_OP_REV'] > 0) &
        (fac_df['DIS_TOT'] > 0) &
        (fac_df['DAY_TOT'] > 0)
    ].copy()
    
    # Engineer annual indicators
    fac_df['OP_MARGIN'] = (fac_df['TOT_OP_REV'] - fac_df['TOT_OP_EXP']) / fac_df['TOT_OP_REV']
    fac_df['EXP_REV_RATIO'] = fac_df['TOT_OP_EXP'] / fac_df['TOT_OP_REV']
    fac_df['REV_PER_BED'] = fac_df['TOT_OP_REV'] / fac_df['AVL_BEDS']
    fac_df['EXP_PER_BED'] = fac_df['TOT_OP_EXP'] / fac_df['AVL_BEDS']
    fac_df['OCCUPANCY_RATE'] = fac_df['DAY_TOT'] / (fac_df['AVL_BEDS'] * 365.25)
    fac_df['STF_AVL_RATIO'] = fac_df['STF_BEDS'] / fac_df['AVL_BEDS']
    fac_df['ALOS'] = fac_df['DAY_TOT'] / fac_df['DIS_TOT']
    fac_df['OUTPATIENT_RATIO'] = fac_df['VIS_TOT'] / fac_df['DAY_TOT']
    
    return fac_df


def prepare_feature_matrix(
    df: pd.DataFrame,
    features: list[str] = FEATURE_NAMES,
    scaler_type: str = 'robust',
    clip_quantiles: tuple[float, float] = (0.01, 0.99)
) -> tuple[np.ndarray, pd.DataFrame, object, pd.DataFrame]:
    """
    Extracts the feature matrix, clips extreme outliers if requested, scales the features,
    and returns scaled matrix X, unscaled feature dataframe, the fitted scaler, and identifier dataframe.
    """
    for f in features:
        if f not in df.columns:
            raise ValueError(f"Feature '{f}' not present in dataframe.")
            
    feature_df = df[features].copy()
    
    # Clip extreme ratio outliers at specified quantiles to protect distance metrics
    clipped_df = feature_df.copy()
    if clip_quantiles:
        low_q, high_q = clip_quantiles
        for col in ['OP_MARGIN', 'EXP_REV_RATIO', 'ALOS', 'OUTPATIENT_RATIO']:
            if col in clipped_df.columns:
                lower = clipped_df[col].quantile(low_q)
                upper = clipped_df[col].quantile(high_q)
                clipped_df[col] = clipped_df[col].clip(lower, upper)
                
    if scaler_type == 'standard':
        scaler = StandardScaler()
    elif scaler_type == 'robust':
        scaler = RobustScaler()
    else:
        raise ValueError(f"Unsupported scaler_type '{scaler_type}'. Choose 'standard' or 'robust'.")
        
    X_scaled = scaler.fit_transform(clipped_df)
    
    # Extract identifiers
    id_cols = [c for c in ['FAC_NO', 'FAC_NAME', 'COUNTY_NAME', 'TYPE_CNTRL', 'TYPE_HOSP', 'QUARTERS_REPORTED', 'AVL_BEDS', 'TOT_OP_REV', 'TOT_OP_EXP'] if c in df.columns]
    id_df = df[id_cols].copy()
    
    return X_scaled, feature_df, scaler, id_df
