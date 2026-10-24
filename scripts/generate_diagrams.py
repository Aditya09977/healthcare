"""
scripts/generate_diagrams.py
Generates high-resolution architectural and workflow diagrams for:
1. Overall End-to-End System Architecture
2. Data Preprocessing & Validation Pipeline
3. Feature Engineering Workflow
4. Clustering & Model Evaluation Pipeline
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_system_architecture(output_path: str):
    """Generates the overall system architecture diagram."""
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Styling constants
    navy = '#0a2540'
    teal = '#007a87'
    light_blue = '#e8f4f8'
    accent_green = '#2e7d32'
    accent_purple = '#5e35b1'
    box_edge = '#1e3d59'

    # Title
    ax.text(6, 5.6, "End-to-End Healthcare Facility Clustering & Analytics Architecture", 
            ha='center', va='center', fontsize=13, fontweight='bold', color=navy)

    # Stages definition: (x, y, width, height, title, subtitle, color)
    blocks = [
        (0.5, 3.2, 1.8, 1.5, "Data Ingestion", "HealthData.gov / HCAI\n5 Quarterly Files\n(2,192 records, 447 fac.)", light_blue, navy),
        (2.7, 3.2, 1.8, 1.5, "Preprocessing", "Schema Validation\nClosed Facility Filter\nMissing & Zero Checks", light_blue, navy),
        (4.9, 3.2, 1.8, 1.5, "Feature Eng.", "Operating Margin\nExpense/Rev Ratio\nRev/Exp per Bed, ALOS\nOccupancy & Staff Ratio", light_blue, navy),
        (7.1, 3.2, 1.8, 1.5, "Scaling & Matrix", "Annualized Aggregation\nOutlier Truncation (1-99%)\nRobustScaler (Median/IQR)", light_blue, navy),
        (9.3, 3.2, 2.2, 1.5, "Clustering Suite", "1. K-Means (k=2..10)\n2. Agglomerative (Ward)\n3. DBSCAN (Grid eps/min)", '#fff3e0', '#d84315'),
        
        # Lower tier
        (2.7, 0.8, 2.2, 1.5, "Internal Validation", "Silhouette Coefficient\nDavies-Bouldin Index\nCalinski-Harabasz Index", '#f3e5f5', accent_purple),
        (5.5, 0.8, 2.4, 1.5, "Cluster Profiling", "Centroid Interpretation\nFacility Archetypes (4 tiers)\nMedians & Statistical Diff", '#e8f5e9', accent_green),
        (8.5, 0.8, 2.5, 1.5, "Interactive Dashboard", "Streamlit Analytics App\nPCA 2D Cluster Explorer\nFinancial Benchmarking", '#e0f2f1', teal)
    ]

    for (x, y, w, h, title, subtitle, bg_col, text_col) in blocks:
        # Draw rounded rectangle
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.15",
            facecolor=bg_col, edgecolor=box_edge, linewidth=1.5
        )
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=text_col)
        ax.text(x + w/2, y + (h - 0.4)/2, subtitle, ha='center', va='center', fontsize=7.5, color='#333333', multialignment='center')

    # Draw arrows
    arrows = [
        # Top row transitions
        ((2.3, 3.95), (2.7, 3.95)),
        ((4.5, 3.95), (4.9, 3.95)),
        ((6.7, 3.95), (7.1, 3.95)),
        ((8.9, 3.95), (9.3, 3.95)),
        # Downward from clustering to validation
        ((10.4, 3.2), (10.4, 2.6)),
        # Bottom row
        ((10.4, 2.6), (3.8, 2.6)),
        ((3.8, 2.6), (3.8, 2.3)),
        ((4.9, 1.55), (5.5, 1.55)),
        ((7.9, 1.55), (8.5, 1.55))
    ]

    for (p1, p2) in arrows:
        ax.annotate('', xy=p2, xytext=p1,
                    arrowprops=dict(arrowstyle="->", color=navy, lw=1.5, shrinkA=2, shrinkB=2))

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def draw_preprocessing_workflow(output_path: str):
    """Generates the preprocessing pipeline diagram."""
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    navy = '#0a2540'
    teal = '#007a87'
    light_gray = '#f8f9fa'

    ax.text(5, 4.6, "Data Preprocessing and Quality Audit Workflow", 
            ha='center', va='center', fontsize=12, fontweight='bold', color=navy)

    steps = [
        (0.6, 2.5, 1.8, 1.4, "Raw Ingestion", "2,192 Quarterly Records\nfrom 5 HCAI Files\n(2023 Q1-Q4, 2024 Q1)"),
        (2.8, 2.5, 1.8, 1.4, "Schema Validation", "Check 15 Key Metrics\nVerify Type Consistency\n& Column Uniformity"),
        (5.0, 2.5, 1.8, 1.4, "Record Exclusions", "Drop 3 Closed Units\nDrop 6 Inactive Records\n(0 Beds / 0 Patients)"),
        (7.2, 2.5, 2.2, 1.4, "Annual Aggregation", "428 Facilities with 4 Qtrs\nSum Annual Financials\nMean Annual Capacities")
    ]

    for (x, y, w, h, title, desc) in steps:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                                      facecolor='#e8f4f8', edgecolor='#007a87', linewidth=1.4)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=navy)
        ax.text(x + w/2, y + (h - 0.4)/2, desc, ha='center', va='center', fontsize=7.5, color='#222222', multialignment='center')

    # Arrows for top row
    for p1, p2 in [((2.4, 3.2), (2.8, 3.2)), ((4.6, 3.2), (5.0, 3.2)), ((6.8, 3.2), (7.2, 3.2))]:
        ax.annotate('', xy=p2, xytext=p1, arrowprops=dict(arrowstyle="->", color=teal, lw=1.5))

    # Bottom final box
    rect_bot = patches.FancyBboxPatch((3.0, 0.6), 4.0, 1.3, boxstyle="round,pad=0.08,rounding_size=0.12",
                                      facecolor='#e8f5e9', edgecolor='#2e7d32', linewidth=1.5)
    ax.add_patch(rect_bot)
    ax.text(5.0, 1.55, "Cleaned Facility Analytical Dataset", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1b5e20')
    ax.text(5.0, 1.05, "428 Validated Hospitals (N=428, 8 Metrics)\nNo Missing Values | Zero-Division Guarded", ha='center', va='center', fontsize=8, color='#333333')

    # Arrow from top row right to bottom
    ax.annotate('', xy=(7.0, 1.3), xytext=(8.3, 2.5), arrowprops=dict(arrowstyle="->", color=teal, lw=1.5, connectionstyle="angle,angleA=0,angleB=90,rad=10"))

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def draw_clustering_workflow(output_path: str):
    """Generates the clustering and model evaluation pipeline diagram."""
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    navy = '#0a2540'
    purple = '#5e35b1'

    ax.text(5, 4.6, "Tri-Algorithm Clustering and Comparative Evaluation Framework", 
            ha='center', va='center', fontsize=12, fontweight='bold', color=navy)

    # Input Box
    r_in = patches.FancyBboxPatch((0.5, 1.8), 2.0, 1.8, boxstyle="round,pad=0.08,rounding_size=0.12",
                                 facecolor='#e8f4f8', edgecolor='#007a87', linewidth=1.4)
    ax.add_patch(r_in)
    ax.text(1.5, 3.25, "Scaled Input Matrix", ha='center', va='center', fontsize=9.5, fontweight='bold', color=navy)
    ax.text(1.5, 2.5, "N = 428 Facilities\nD = 8 Indicators\nScaled with RobustScaler\n(Median & IQR)", ha='center', va='center', fontsize=7.5, color='#333333')

    # 3 Algorithm boxes
    algs = [
        (3.3, 3.2, 2.5, 1.1, "1. K-Means", "k in [2..10]\n10 inits, k-means++\nEuclidean distance"),
        (3.3, 1.9, 2.5, 1.1, "2. Agglomerative", "k in [2..10]\nWard / Average / Complete\nBottom-up merge"),
        (3.3, 0.6, 2.5, 1.1, "3. DBSCAN", "eps in [0.8..2.5]\nmin_samples in [3..10]\nDensity core / noise")
    ]

    for (x, y, w, h, title, desc) in algs:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.1",
                                      facecolor='#fff8e1', edgecolor='#f57c00', linewidth=1.3)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.28, title, ha='center', va='center', fontsize=9, fontweight='bold', color='#e65100')
        ax.text(x + w/2, y + (h - 0.35)/2, desc, ha='center', va='center', fontsize=7, color='#333333')
        # Arrow from input
        ax.annotate('', xy=(x, y + h/2), xytext=(2.5, 2.7), arrowprops=dict(arrowstyle="->", color=navy, lw=1.2))

    # Evaluation Box
    r_eval = patches.FancyBboxPatch((6.6, 1.5), 2.8, 2.4, boxstyle="round,pad=0.08,rounding_size=0.12",
                                    facecolor='#f3e5f5', edgecolor=purple, linewidth=1.5)
    ax.add_patch(r_eval)
    ax.text(8.0, 3.55, "Evaluation & Selection", ha='center', va='center', fontsize=9.5, fontweight='bold', color=purple)
    ax.text(8.0, 2.75, "1. Silhouette Score: S(i)\n2. Davies-Bouldin: R_ij\n3. Calinski-Harabasz: B/W\n4. Cluster Size Balance\n5. Clinical Interpretability", ha='center', va='center', fontsize=7.5, color='#333333')
    ax.text(8.0, 1.85, "Selected: K-Means (k=4)\nSil=0.611, DB=0.577, CH=655.8", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#4a148c')

    # Arrows to evaluation
    for (x, y, w, h, _, _) in algs:
        ax.annotate('', xy=(6.6, 2.7), xytext=(x + w, y + h/2), arrowprops=dict(arrowstyle="->", color=purple, lw=1.2))

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


if __name__ == '__main__':
    figures_dir = os.path.join("figures")
    docs_diag_dir = os.path.join("docs", "diagrams")
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(docs_diag_dir, exist_ok=True)

    arch_fig = os.path.join(figures_dir, "architecture_diagram.png")
    draw_system_architecture(arch_fig)
    draw_system_architecture(os.path.join(docs_diag_dir, "architecture_diagram.png"))

    prep_fig = os.path.join(figures_dir, "preprocessing_workflow.png")
    draw_preprocessing_workflow(prep_fig)
    draw_preprocessing_workflow(os.path.join(docs_diag_dir, "preprocessing_workflow.png"))

    clust_fig = os.path.join(figures_dir, "clustering_workflow.png")
    draw_clustering_workflow(clust_fig)
    draw_clustering_workflow(os.path.join(docs_diag_dir, "clustering_workflow.png"))
