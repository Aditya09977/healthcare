"""
src/clustering.py
Clustering Implementation Module for Healthcare Facility Analytics.

Implements and benchmarks exactly three unsupervised learning algorithms:
1. K-Means Clustering (baseline with multiple initializations and fixed random seed)
2. Agglomerative Hierarchical Clustering (Ward, average, and complete linkage)
3. DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from scipy.cluster.hierarchy import linkage


def run_kmeans(X: np.ndarray, k: int, random_state: int = 42, n_init: int = 10) -> tuple[KMeans, np.ndarray, float]:
    """
    Fits K-Means clustering algorithm for a given number of clusters k.
    Returns the fitted estimator, cluster labels, and inertia (within-cluster sum of squares).
    """
    model = KMeans(n_clusters=k, random_state=random_state, n_init=n_init)
    labels = model.fit_predict(X)
    inertia = float(model.inertia_)
    return model, labels, inertia


def run_agglomerative(X: np.ndarray, k: int, linkage_type: str = 'ward') -> tuple[AgglomerativeClustering, np.ndarray]:
    """
    Fits Agglomerative Hierarchical Clustering for a given cluster count k and linkage strategy.
    Note: Ward linkage strictly requires Euclidean metric.
    """
    if linkage_type == 'ward':
        model = AgglomerativeClustering(n_clusters=k, linkage='ward')
    elif linkage_type in ['average', 'complete']:
        model = AgglomerativeClustering(n_clusters=k, linkage=linkage_type, metric='euclidean')
    else:
        raise ValueError(f"Unsupported linkage type: {linkage_type}. Choose 'ward', 'average', or 'complete'.")
        
    labels = model.fit_predict(X)
    return model, labels


def compute_hierarchical_linkage(X: np.ndarray, method: str = 'ward') -> np.ndarray:
    """
    Computes hierarchical clustering linkage matrix using SciPy for dendrogram visualization.
    """
    return linkage(X, method=method)


def run_dbscan(X: np.ndarray, eps: float, min_samples: int) -> tuple[DBSCAN, np.ndarray, int, float]:
    """
    Fits DBSCAN clustering algorithm.
    Returns fitted model, cluster labels, number of core clusters (excluding noise -1),
    and noise percentage.
    """
    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(X)
    
    unique_labels = set(labels)
    n_noise = int((labels == -1).sum())
    n_clusters = len(unique_labels - {-1})
    noise_ratio = (n_noise / len(labels)) * 100.0 if len(labels) > 0 else 0.0
    
    return model, labels, n_clusters, noise_ratio
