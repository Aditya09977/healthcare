"""
scripts/generate_notebook.py
Generates the complete Jupyter Notebook 'healthcare_analysis.ipynb'.
"""

import json
import os


def build_notebook():
    nb = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.9"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    def add_md(text):
        nb["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in text.strip().split("\n")]
        })

    def add_code(code_str):
        nb["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in code_str.strip().split("\n")]
        })

    # Cell 1: Markdown Title
    add_md("""# Healthcare Facility Financial and Resource Utilization Pattern Analysis
### CA3 Machine Learning Mini-Project
**Candidate:** Aditya09977  
**Dataset:** California Department of Health Care Access and Information (HCAI) / HealthData.gov (ID: 8j3z-qxvr)  
**Algorithms:** K-Means, Agglomerative Hierarchical Clustering, DBSCAN  
**Evaluation Metrics:** Silhouette Score, Davies–Bouldin Index, Calinski–Harabasz Index  
""")

    # Cell 2: Imports
    add_code("""import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram

# Set visualization styles
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
%matplotlib inline

# Import custom modular src components
from src.preprocessing import (
    load_raw_dataset,
    clean_quarterly_data,
    build_facility_annual_profiles,
    prepare_feature_matrix,
    FEATURE_NAMES,
    FEATURE_DESCRIPTIONS
)
from src.clustering import (
    run_kmeans,
    run_agglomerative,
    compute_hierarchical_linkage,
    run_dbscan
)
from src.evaluation import (
    evaluate_clustering,
    generate_cluster_profiles
)

print("Libraries imported successfully!")
""")

    # Cell 3: Data Ingestion Markdown
    add_md("""## 1. Data Ingestion & Quality Audit
We load the raw quarterly filings from `data/raw/combined_quarterly_raw.csv` (2,192 observations across 5 quarters).
We audit missingness, inspect data types, and filter closed or inactive facilities.
""")

    # Cell 4: Data Ingestion Code
    add_code("""raw_df = load_raw_dataset()
clean_qtr_df, audit_log = clean_quarterly_data(raw_df)

print(f"Total raw filings: {audit_log['total_raw_records']}")
print(f"Closed facilities excluded: {audit_log['closed_facilities_excluded']}")
print(f"Zero capacity/activity records excluded: {audit_log['zero_capacity_or_utilization_excluded']}")
print(f"Valid quarterly records: {audit_log['clean_quarterly_records']} across {audit_log['unique_clean_facilities']} facilities.")
""")

    # Cell 5: Annual Facility Profiles Markdown
    add_md("""## 2. Annualized Facility Profiles (Calendar Year 2023)
To prevent seasonal autocorrelation, we aggregate all 4 quarters of calendar year 2023 for facilities that reported throughout the year (N = 428).
""")

    # Cell 6: Annual Facility Profiles Code
    add_code("""fac_df = build_facility_annual_profiles(clean_qtr_df, target_year=2023)
print(f"Validated facilities with 4 complete quarters: {len(fac_df)}")

# Preview key columns
cols_preview = ['FAC_NO', 'FAC_NAME', 'COUNTY_NAME', 'TYPE_CNTRL', 'AVL_BEDS', 'TOT_OP_REV', 'TOT_OP_EXP']
fac_df[cols_preview].head()
""")

    # Cell 7: Feature Engineering Markdown
    add_md("""## 3. Feature Engineering & Robust Scaling
We compute 8 operational and financial indicators:
- `OP_MARGIN`: (Operating Revenue - Operating Expenses) / Operating Revenue
- `EXP_REV_RATIO`: Operating Expenses / Operating Revenue
- `REV_PER_BED`: Operating Revenue / Available Beds ($)
- `EXP_PER_BED`: Operating Expenses / Available Beds ($)
- `OCCUPANCY_RATE`: Total Patient Days / (Available Beds * 365.25)
- `STF_AVL_RATIO`: Staffed Beds / Available Beds
- `ALOS`: Inpatient Days / Discharges (Days)
- `OUTPATIENT_RATIO`: Outpatient Visits / Inpatient Days
""")

    # Cell 8: Feature Engineering Code
    add_code("""X_scaled, feature_df, scaler, id_df = prepare_feature_matrix(
    fac_df,
    features=FEATURE_NAMES,
    scaler_type='robust',
    clip_quantiles=(0.01, 0.99)
)

print(f"Scaled feature matrix shape: {X_scaled.shape}")
feature_df.describe().T[['mean', 'std', 'min', '50%', 'max']]
""")

    # Cell 9: Correlation Matrix
    add_code("""plt.figure(figsize=(8, 6), dpi=150)
sns.heatmap(feature_df.corr(), annot=True, fmt='.2f', cmap='vlag', vmin=-1, vmax=1)
plt.title("Correlation Matrix of Facility Indicators", fontsize=12, fontweight='bold')
plt.show()
""")

    # Cell 10: Clustering Experiments Markdown
    add_md("""## 4. Machine Learning Clustering Suite
We evaluate three core unsupervised clustering algorithms:
1. **K-Means Clustering** (k = 2 to 10)
2. **Agglomerative Hierarchical Clustering** (Ward, Average, and Complete linkage)
3. **DBSCAN** (Grid search of epsilon and min_samples)
""")

    # Cell 11: K-Means Experiments
    add_code("""kmeans_results = []
for k in range(2, 11):
    model, labels, inertia = run_kmeans(X_scaled, k=k, random_state=42, n_init=10)
    eval_res = evaluate_clustering(X_scaled, labels)
    kmeans_results.append({
        'k': k,
        'Inertia': inertia,
        'Silhouette': eval_res['silhouette'],
        'Davies_Bouldin': eval_res['davies_bouldin'],
        'Calinski_Harabasz': eval_res['calinski_harabasz']
    })

km_df = pd.DataFrame(kmeans_results)
km_df
""")

    # Cell 12: Elbow & Silhouette Plot
    add_code("""fig, ax1 = plt.subplots(figsize=(8, 4.5), dpi=150)
ax1.plot(km_df['k'], km_df['Inertia'], marker='o', color='#0a2540', label='Inertia')
ax1.set_xlabel('Number of Clusters (k)', fontweight='bold')
ax1.set_ylabel('Inertia (WCSS)', color='#0a2540', fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.5)

ax2 = ax1.twinx()
ax2.plot(km_df['k'], km_df['Silhouette'], marker='s', color='#007a87', linestyle='--', label='Silhouette')
ax2.set_ylabel('Silhouette Score', color='#007a87', fontweight='bold')

plt.title('K-Means Elbow Curve and Silhouette Trajectory', fontsize=12, fontweight='bold')
plt.show()
""")

    # Cell 13: Agglomerative Hierarchical Clustering Code
    add_code("""agg_results = []
for linkage_type in ['ward', 'average', 'complete']:
    for k in range(2, 11):
        model, labels = run_agglomerative(X_scaled, k=k, linkage_type=linkage_type)
        eval_res = evaluate_clustering(X_scaled, labels)
        agg_results.append({
            'Linkage': linkage_type.capitalize(),
            'k': k,
            'Silhouette': eval_res['silhouette'],
            'Davies_Bouldin': eval_res['davies_bouldin'],
            'Calinski_Harabasz': eval_res['calinski_harabasz']
        })

pd.DataFrame(agg_results).sort_values(by='Silhouette', ascending=False).head(10)
""")

    # Cell 14: Dendrogram Plot
    add_code("""linkage_mat = compute_hierarchical_linkage(X_scaled, method='ward')
plt.figure(figsize=(10, 4.5), dpi=150)
dendrogram(linkage_mat, truncate_mode='lastp', p=25, leaf_rotation=90., leaf_font_size=9., show_contracted=True)
plt.title("Agglomerative Dendrogram (Ward Linkage, Top 25 Branches)", fontsize=12, fontweight='bold')
plt.xlabel("Cluster Size / Observation Index")
plt.ylabel("Ward Euclidean Linkage Distance")
plt.show()
""")

    # Cell 15: DBSCAN Grid Code
    add_code("""db_results = []
for eps in [0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5]:
    for ms in [3, 5, 8, 10]:
        model, labels, n_cl, noise_pct = run_dbscan(X_scaled, eps=eps, min_samples=ms)
        eval_res = evaluate_clustering(X_scaled, labels, is_dbscan=True)
        db_results.append({
            'eps': eps,
            'min_samples': ms,
            'k_clusters': n_cl,
            'Noise_Pct': noise_pct,
            'Silhouette': eval_res['silhouette'],
            'Davies_Bouldin': eval_res['davies_bouldin']
        })

pd.DataFrame(db_results).dropna(subset=['Silhouette']).head(10)
""")

    # Cell 16: Final Model Selection & Profiling Markdown
    add_md("""## 5. Final Model Selection & Cluster Profiling
We select **K-Means with k = 4** as the final architecture because it avoids the monolithic 97% catch-all grouping of k=2 while generating four distinct, actionable hospital archetypes.
""")

    # Cell 17: Cluster Profiles Code
    add_code("""selected_model, selected_labels, _ = run_kmeans(X_scaled, k=4, random_state=42)
profile_summary, enriched_fac_df = generate_cluster_profiles(
    feature_df,
    selected_labels,
    id_df=id_df,
    cluster_col_name='Cluster'
)

# Display cluster summary table
cols_show = ['Cluster', 'Count', 'Pct_of_Total', 'OP_MARGIN_median', 'EXP_REV_RATIO_median', 'REV_PER_BED_median', 'OCCUPANCY_RATE_median', 'ALOS_median', 'Avg_Available_Beds']
profile_summary[cols_show]
""")

    # Cell 18: 2D PCA Cluster Projection Code
    add_code("""pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)
var_exp = pca.explained_variance_ratio_ * 100.0

plt.figure(figsize=(8, 5), dpi=150)
for c in range(4):
    mask = (selected_labels == c)
    plt.scatter(X_pca[mask, 0], X_pca[mask, 1], label=f'Cluster {c} (N={mask.sum()})', alpha=0.75, s=40)

centroids_pca = pca.transform(selected_model.cluster_centers_)
plt.scatter(centroids_pca[:, 0], centroids_pca[:, 1], marker='X', s=150, c='black', label='Centroids')

plt.title(f'2D PCA Projection of Healthcare Facility Clusters (k=4)', fontsize=12, fontweight='bold')
plt.xlabel(f'PC1 ({var_exp[0]:.1f}% Variance)')
plt.ylabel(f'PC2 ({var_exp[1]:.1f}% Variance)')
plt.legend()
plt.show()
""")

    # Cell 19: Conclusion Markdown
    add_md("""## 6. Synthesis of Four Healthcare Facility Archetypes
1. **Cluster 0: General Acute Care Hospitals (90.7%)** — Core community and regional acute care facilities operating on narrow margins (+0.93%) with standard acute stays (5.7 days).
2. **Cluster 1: State / Long-Term Institutional Hospitals (1.9%)** — Large bed capacity (~795 beds), high occupancy (92.0%), extreme stays (403 days), operating at subsidized accounting deficits.
3. **Cluster 2: Subacute & Extended Recovery Care (2.8%)** — Extended rehabilitation stays (122 days) and moderate bed capacity.
4. **Cluster 3: High-Intensity Specialized Surgical Centers (4.7%)** — Compact bed size (~40 beds), short stays (3.6 days), very high revenue per bed ($3.58M).
""")

    out_path = "healthcare_analysis.ipynb"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)

    print(f"Successfully generated Jupyter Notebook: {out_path}")


if __name__ == '__main__':
    build_notebook()
