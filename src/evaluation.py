"""
src/evaluation.py
Clustering Evaluation and Facility Profile Generation Module.

Computes internal cluster validity metrics:
1. Silhouette Score (higher is better, range [-1, 1])
2. Davies-Bouldin Index (lower is better, range [0, inf))
3. Calinski-Harabasz Index (higher is better, range [0, inf))

Also generates evidence-based cluster profiles, centroid comparisons,
and exports experiment results to CSV.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


def evaluate_clustering(X: np.ndarray, labels: np.ndarray, is_dbscan: bool = False) -> dict:
    """
    Evaluates cluster quality using internal validity metrics.
    Gracefully handles edge cases (e.g. single cluster, all noise).
    """
    results = {
        'n_clusters': 0,
        'silhouette': np.nan,
        'davies_bouldin': np.nan,
        'calinski_harabasz': np.nan,
        'noise_points': 0,
        'noise_ratio_pct': 0.0,
        'valid_metrics': False,
        'notes': ''
    }
    
    unique_labels = set(labels)
    n_total = len(labels)
    
    if is_dbscan:
        n_noise = int((labels == -1).sum())
        core_labels = unique_labels - {-1}
        n_clusters = len(core_labels)
        noise_pct = (n_noise / n_total) * 100.0 if n_total > 0 else 0.0
        
        results['n_clusters'] = n_clusters
        results['noise_points'] = n_noise
        results['noise_ratio_pct'] = round(noise_pct, 2)
        
        # Valid metrics require at least 2 distinct clusters in non-noise points
        if n_clusters < 2:
            results['notes'] = f"DBSCAN generated {n_clusters} clusters; minimum 2 required for internal validity scoring."
            return results
            
        # Evaluate metrics on non-noise points
        mask = (labels != -1)
        X_eval = X[mask]
        labels_eval = labels[mask]
        
        if len(set(labels_eval)) < 2 or len(labels_eval) <= n_clusters:
            results['notes'] = "Insufficient non-noise points per cluster for scoring."
            return results
    else:
        n_clusters = len(unique_labels)
        results['n_clusters'] = n_clusters
        X_eval = X
        labels_eval = labels
        
        if n_clusters < 2 or n_clusters >= n_total:
            results['notes'] = f"Invalid cluster count ({n_clusters}) for dataset of size {n_total}."
            return results

    try:
        results['silhouette'] = float(silhouette_score(X_eval, labels_eval))
        results['davies_bouldin'] = float(davies_bouldin_score(X_eval, labels_eval))
        results['calinski_harabasz'] = float(calinski_harabasz_score(X_eval, labels_eval))
        results['valid_metrics'] = True
        results['notes'] = 'Evaluation computed successfully.'
    except Exception as e:
        results['notes'] = f"Error computing metrics: {str(e)}"
        
    return results


def generate_cluster_profiles(
    df_features: pd.DataFrame,
    labels: np.ndarray,
    id_df: pd.DataFrame = None,
    cluster_col_name: str = 'Cluster'
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generates quantitative profile summaries for each identified cluster.
    Returns:
    1. Numeric cluster summary table with mean and median across all indicators
    2. Enriched observation dataframe with assigned cluster labels
    """
    combined_df = df_features.copy()
    if id_df is not None:
        for c in id_df.columns:
            if c not in combined_df.columns:
                combined_df[c] = id_df[c].values
                
    combined_df[cluster_col_name] = labels
    
    unique_clusters = sorted(list(set(labels)))
    profile_rows = []
    
    total_obs = len(combined_df)
    
    # Dataset overall baseline
    baseline_stats = {'Cluster': 'Overall Dataset', 'Count': total_obs, 'Pct_of_Total': 100.0}
    for col in df_features.columns:
        baseline_stats[f"{col}_mean"] = combined_df[col].mean()
        baseline_stats[f"{col}_median"] = combined_df[col].median()
    profile_rows.append(baseline_stats)
    
    # Per-cluster statistics
    for cl in unique_clusters:
        cl_mask = (combined_df[cluster_col_name] == cl)
        cl_df = combined_df[cl_mask]
        count = len(cl_df)
        pct = (count / total_obs) * 100.0
        
        cl_label = f"Noise (Cluster -1)" if cl == -1 else f"Cluster {cl}"
        cl_stats = {
            'Cluster': cl_label,
            'Count': count,
            'Pct_of_Total': round(pct, 2)
        }
        
        for col in df_features.columns:
            cl_stats[f"{col}_mean"] = cl_df[col].mean()
            cl_stats[f"{col}_median"] = cl_df[col].median()
            
        # Additional operational metadata if available in id_df
        if 'AVL_BEDS' in combined_df.columns:
            cl_stats['Avg_Available_Beds'] = cl_df['AVL_BEDS'].mean()
        if 'TOT_OP_REV' in combined_df.columns:
            cl_stats['Avg_Annual_Revenue_M'] = cl_df['TOT_OP_REV'].mean() / 1e6
        if 'TOT_OP_EXP' in combined_df.columns:
            cl_stats['Avg_Annual_Expense_M'] = cl_df['TOT_OP_EXP'].mean() / 1e6
            
        profile_rows.append(cl_stats)
        
    summary_df = pd.DataFrame(profile_rows)
    return summary_df, combined_df
