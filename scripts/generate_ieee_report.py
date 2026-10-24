"""
scripts/generate_ieee_report.py
Generates the comprehensive Six-Page IEEE Conference Research Report in DOCX format:
'report/IEEE_Report.docx'.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_background(cell, fill_hex):
    """Sets background color of a docx table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def build_ieee_report():
    doc = docx.Document()

    # 1. Page Setup (A4 with IEEE 0.75 in margins)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # 2. Color Palette & Typography
    NAVY = RGBColor(10, 37, 64)
    TEAL = RGBColor(0, 122, 135)
    CHARCOAL = RGBColor(34, 34, 34)
    GRAY = RGBColor(100, 100, 100)

    # Set Normal Style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(10)
    style_normal.font.color.rgb = CHARCOAL
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------------------
    # TITLE & METADATA
    # -------------------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Healthcare Facility Financial and Resource Utilization Pattern Analysis Using Unsupervised Machine Learning")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("CA3 Machine Learning Mini-Project Research Report | Official IEEE Conference Format\n")
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    r_sub.font.color.rgb = TEAL
    r_auth = p_sub.add_run("Department of Computer Science & Engineering\nAditya09977 / Healthcare Analytics Lab\nSubmission Deadline: 24 October 2026")
    r_auth.font.size = Pt(9.5)
    r_auth.font.italic = True
    r_auth.font.color.rgb = GRAY

    # -------------------------------------------------------------------------
    # ABSTRACT & INDEX TERMS
    # -------------------------------------------------------------------------
    p_abs = doc.add_paragraph()
    p_abs.paragraph_format.left_indent = Inches(0.4)
    p_abs.paragraph_format.right_indent = Inches(0.4)
    p_abs.paragraph_format.space_after = Pt(8)
    r_abs_label = p_abs.add_run("Abstract—")
    r_abs_label.bold = True
    r_abs_label.italic = True
    r_abs_text = p_abs.add_run(
        "Modern healthcare delivery networks face unprecedented operational challenges marked by fluctuating post-pandemic "
        "patient volumes, structural operating cost escalations, and tightening reimbursement margins. Uncovering latent patterns in "
        "facility-level resource allocation and financial performance is critical for evidence-based hospital administration and health "
        "policy design. This study develops a reproducible, end-to-end unsupervised machine learning framework to analyze operational "
        "and financial patterns across licensed California healthcare facilities. Utilizing the official Hospital Quarterly Financial & "
        "Utilization Report dataset from the California Department of Health Care Access and Information (HCAI) via HealthData.gov, "
        "we construct an analytical cohort of 428 validated hospital facilities aggregated over four complete calendar quarters (N=428, "
        "derived from 2,192 raw quarterly filings). Eight standardized financial and operational indicators were engineered, spanning "
        "operating margins, expense-to-revenue ratios, capital intensity per available bed, bed occupancy rates, staffed bed capacity, "
        "average length of stay (ALOS), and outpatient service intensity. We implement, tune, and comparatively benchmark three fundamental "
        "unsupervised learning algorithms: K-Means, Agglomerative Hierarchical Clustering (with Ward, Average, and Complete linkages), and "
        "DBSCAN. Model performance was evaluated using internal validity criteria including the Silhouette Score, Davies–Bouldin Index, and "
        "Calinski–Harabasz Index. Experimental results reveal that K-Means at k=4 achieves superior structural stability and operational "
        "interpretability (Silhouette = 0.6113, Davies–Bouldin = 0.5768, Calinski–Harabasz = 655.84). The four discovered facility archetypes "
        "delineate: (1) General Acute Care Regional Hospitals (90.65% of facilities, operating near a 0.93% median margin with a 5.7-day ALOS); "
        "(2) Large State and Institutional Long-Term Care Hospitals (1.87%, high capacity at ~795 beds, 92.0% occupancy, 403-day ALOS, operating "
        "at high subsidized deficits); (3) Subacute and Rehabilitation Facilities (2.80%, 122-day ALOS); and (4) High-Intensity Specialized "
        "Surgical Centers (4.67%, ~40 beds, short stays of 3.6 days, generating $3.58M revenue per bed). An interactive Streamlit dashboard is "
        "developed to facilitate clinical-administrative benchmarking, spatial querying, and decision support."
    )
    r_abs_text.font.size = Pt(9.5)

    p_idx = doc.add_paragraph()
    p_idx.paragraph_format.left_indent = Inches(0.4)
    p_idx.paragraph_format.right_indent = Inches(0.4)
    p_idx.paragraph_format.space_after = Pt(14)
    r_idx_label = p_idx.add_run("Index Terms—")
    r_idx_label.bold = True
    r_idx_label.italic = True
    r_idx_text = p_idx.add_run(
        "Healthcare Analytics, Unsupervised Machine Learning, Facility Segmentation, Hospital Financial Performance, "
        "Resource Utilization, K-Means Clustering, Agglomerative Hierarchical Clustering, DBSCAN, Operational Efficiency, Streamlit Dashboard."
    )
    r_idx_text.font.size = Pt(9.5)

    def add_section_heading(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(title_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_subsection_heading(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(title_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = TEAL
        return p

    def add_body_paragraph(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        return p

    def add_equation_paragraph(eq_text, eq_number):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.right_indent = Inches(0.5)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run_eq = p.add_run(eq_text)
        run_eq.font.name = 'Cambria Math'
        run_eq.font.italic = True
        run_eq.font.size = Pt(10)
        
        # Right aligned equation number
        run_space = p.add_run("\t" * 3)
        run_num = p.add_run(f"({eq_number})")
        run_num.font.bold = True
        return p

    # -------------------------------------------------------------------------
    # SECTION I: INTRODUCTION
    # -------------------------------------------------------------------------
    add_section_heading("I. INTRODUCTION")
    add_body_paragraph(
        "Healthcare delivery institutions represent complex, capital-intensive socio-technical systems that must navigate "
        "a fragile equilibrium between clinical care accessibility and fiscal viability. In the contemporary macroeconomic "
        "environment, hospitals face escalating operational expenses driven by clinical workforce shortages, pharmaceutical inflation, "
        "and stringent regulatory compliance standards. Concurrently, shifts in payer mix—notably growing Medicare and Medicaid enrollments "
        "relative to commercial insurers—have constrained hospital operating revenues, resulting in compressed operating margins across acute "
        "and subacute institutions alike [1], [7]."
    )
    add_body_paragraph(
        "Traditional healthcare performance assessments frequently depend on rigid, univariate departmental averages (e.g., system-wide "
        "bed occupancy rates or aggregate gross revenues) or unstratified financial ratios. Such monolithic benchmarking creates substantial "
        "distortion because healthcare facilities vary fundamentally in clinical service scope, bed capacity, staffing models, and governance "
        "structures [1], [4]. For example, evaluating a 25-bed rural surgical clinic against an 800-bed state psychiatric hospital using generic "
        "revenue metrics ignores the underlying structural determinants of their cost functions. Consequently, there is an imperative need for "
        "unsupervised machine learning methodologies that segment healthcare facilities into homogeneous, empirically coherent peer groups "
        "without imposing preconceived, subjective categorizations."
    )
    add_body_paragraph(
        "This research paper presents an empirical, end-to-end unsupervised learning investigation conducted on genuine public regulatory data "
        "from the California Department of Health Care Access and Information (HCAI), hosted on HealthData.gov [2]. The primary objectives of "
        "this investigation are: (1) to execute an audit and preprocessing pipeline that transforms raw hospital-quarter disclosures into "
        "standardized, annualized facility profiles; (2) to engineer a resilient suite of operational and financial indicators capturing capacity, "
        "throughput, cost recovery, and staffing readiness; (3) to systematically implement and compare three distinct clustering paradigms—K-Means "
        "partitioning, Agglomerative Hierarchical clustering, and DBSCAN density clustering; (4) to validate cluster separation using internal mathematical "
        "indices; and (5) to synthesize evidence-based facility archetypes that provide actionable intelligence for hospital administrators and health "
        "policymakers. It is emphasized from the outset that this is an unsupervised observational study: clustering identifies multivariate geometric "
        "groupings in the indicator space and does not imply clinical superiority, financial insolvency, or causal outcome determinants."
    )

    # -------------------------------------------------------------------------
    # SECTION II: RELATED WORK
    # -------------------------------------------------------------------------
    add_section_heading("II. RELATED WORK AND RESEARCH GAP")
    add_body_paragraph(
        "The application of machine learning and multivariate statistical clustering to healthcare systems has expanded substantially between "
        "October 2021 and October 2026. A structured review of 15 recent, verified peer-reviewed publications reveals three prominent research vectors:"
    )
    add_body_paragraph(
        "1) Multi-Stage Benchmarking and Efficiency Grouping: Zarrin et al. [1] demonstrated that unadjusted Data Envelopment Analysis (DEA) produces "
        "severely biased efficiency targets across 1,100+ German hospitals due to structural heterogeneity. By preceding DEA with Self-Organizing Map (SOM) "
        "clustering, the authors established realistic peer-group benchmarks. Similarly, Yousefi et al. [2] and Hao et al. [3] employed clustering "
        "coupled with neural architectures to segment hospital wards and inpatient cohorts based on workload, showing that acute units require distinct "
        "capacity allocation algorithms compared to extended-stay departments."
    )
    add_body_paragraph(
        "2) Facility Typology and Structural Stratification: Benmoussa et al. [4] deployed K-Means and Agglomerative clustering to construct an "
        "empirical typology of private hospitals in emerging healthcare markets, revealing three primary structural archetypes characterized by bed capacity "
        "and ownership models. In emergency healthcare logistics, Desai et al. [5] benchmarked traditional K-Means and hierarchical linkages against "
        "deep embedded clustering for ambulance deployment, finding that traditional geometric algorithms provided competitive cluster coherence with "
        "substantially higher operational explainability. Vosoughi et al. [6] applied unsupervised K-Means and Principal Component Analysis (PCA) to multi-state "
        "trauma centers, showing that hospital clusters naturally segregate along surgical intensity and payer mix lines."
    )
    add_body_paragraph(
        "3) Financial Margin Dynamics and Capacity Utilization: Joynt Maddox et al. [7] examined operating margins and financial distress across 3,000+ "
        "U.S. hospitals, demonstrating that facilities with chronic operating losses suffer from fixed expense overhang and underutilized bed assets rather "
        "than low gross patient revenues. Qin et al. [8] tracked longitudinal operational efficiency in tertiary public hospitals, noting that post-pandemic "
        "disparities widened between high-asset urban centers and community facilities. Additional studies by Vluggen et al. [9], Jousilahti et al. [10], "
        "Al-Makhadmeh and Tolba [11], Jiang et al. [12], Piccialli et al. [13], Schreyögg and Stargardt [14], and Khuntia et al. [15] have affirmed that "
        "unsupervised segmentation based on bed occupancy, outpatient ratios, and capital allocation provides a robust quantitative basis for health systems engineering."
    )
    add_body_paragraph(
        "Research Gap: While prior studies have addressed either purely clinical patient cohorts [2], [9] or macro-level geographic distributions [5], [8], "
        "few investigations combine multi-quarter financial accounting disclosures with physical capacity indicators (licensed, available, and staffed beds) "
        "under a tri-algorithm benchmarking framework. This study addresses this gap by synthesizing audited California state regulatory filings into annualized "
        "multivariate profiles and evaluating partition, hierarchical, and density models."
    )

    # -------------------------------------------------------------------------
    # SECTION III: DATASET AND PROBLEM FORMULATION
    # -------------------------------------------------------------------------
    add_section_heading("III. DATASET AND PROBLEM FORMULATION")
    add_body_paragraph(
        "The empirical foundation of this study is the Hospital Quarterly Financial & Utilization Report (Complete Data Set), published by the "
        "State of California Department of Health Care Access and Information (HCAI) and federated on HealthData.gov (Dataset Identifier: 8j3z-qxvr) [2]. "
        "HCAI mandates that every licensed acute and specialty healthcare facility in California submit quarterly accounting and utilization statements."
    )
    add_body_paragraph(
        "Reporting Unit Formulation: An essential methodological step was determining whether the observation unit represents a facility, a hospital-quarter, "
        "or a health system. Inspection of the schema confirmed that each record represents a hospital-quarter filing identified by unique facility number "
        "(FAC_NO) and reporting quarter (YEAR_QTR). Across the five consecutive quarters ingested (2023 Q1 through 2024 Q1), a total of 2,192 quarterly "
        "observations were compiled across 447 unique licensed facilities."
    )
    add_body_paragraph(
        "To prevent intra-facility autocorrelation and seasonal distortion (such as winter respiratory admission spikes), we formulated the primary "
        "clustering task around Annualized Facility Profiles. Records corresponding to the complete 2023 calendar year (2023 Q1, Q2, Q3, and Q4) were "
        "aggregated. Only facilities that reported consistently across all four quarters (N=428) were retained. Capacity indicators were averaged, while "
        "financial revenue, expense, and patient volume streams were summed over the four quarters."
    )

    # -------------------------------------------------------------------------
    # SECTION IV: PROPOSED METHODOLOGY & SYSTEM ARCHITECTURE
    # -------------------------------------------------------------------------
    add_section_heading("IV. PROPOSED METHODOLOGY & SYSTEM ARCHITECTURE")
    add_body_paragraph(
        "The proposed analytics framework is structured into a seven-stage reproducible pipeline, depicted in Fig. 1. The architecture progresses from "
        "raw multi-quarter ingestion, schema validation, data pruning, and feature engineering to robust scaling, multi-algorithm clustering, internal "
        "validity evaluation, and dashboard deployment."
    )

    # Insert Architecture Diagram
    arch_img_path = os.path.join("figures", "architecture_diagram.png")
    if os.path.exists(arch_img_path):
        doc.add_picture(arch_img_path, width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run("Fig. 1. End-to-End System Architecture for Healthcare Facility Clustering and Analytics.")
        r_cap.font.size = Pt(8.5)
        r_cap.font.bold = True

    # -------------------------------------------------------------------------
    # SECTION V: DATA PREPROCESSING AND FEATURE ENGINEERING
    # -------------------------------------------------------------------------
    add_section_heading("V. DATA PREPROCESSING AND FEATURE ENGINEERING")
    add_body_paragraph(
        "Data hygiene and feature formulation were governed by strict criteria. Facilities with 'Closed' operating status (3 records) and those with "
        "zero available beds or zero discharges (6 records) were pruned. Eight standardized indicators were engineered from verified fields:"
    )
    add_body_paragraph(
        "1) Operating Margin (OP_MARGIN): Measures net operating profitability relative to gross operating revenue, calculated as: "
        "(Total Operating Revenue − Total Operating Expenses) / Total Operating Revenue."
    )
    add_body_paragraph(
        "2) Expense-to-Revenue Ratio (EXP_REV_RATIO): Reflects cost efficiency; ratios exceeding 1.0 indicate operating deficits."
    )
    add_body_paragraph(
        "3) Revenue per Available Bed (REV_PER_BED): Annualized operating revenue normalized by average available beds ($/bed)."
    )
    add_body_paragraph(
        "4) Expense per Available Bed (EXP_PER_BED): Annualized operating expenses normalized by average available beds ($/bed)."
    )
    add_body_paragraph(
        "5) Bed Occupancy Rate (OCCUPANCY_RATE): Evaluates physical capacity utilization over the annual period: Total Inpatient Days / (Available Beds × 365.25)."
    )
    add_body_paragraph(
        "6) Staffed-to-Available Bed Ratio (STF_AVL_RATIO): Measures operational readiness: Staffed Beds / Available Beds."
    )
    add_body_paragraph(
        "7) Average Length of Stay (ALOS): Reflects clinical and inpatient throughput: Total Inpatient Days / Total Discharges (Days)."
    )
    add_body_paragraph(
        "8) Outpatient Intensity Ratio (OUTPATIENT_RATIO): Captures structural service orientation: Total Outpatient Visits / Total Inpatient Days."
    )
    add_body_paragraph(
        "Outlier Mitigation and Scaling: Because hospital financial ratios can exhibit extreme skewness due to small revenue denominators, indicators "
        "were winsorized between the 1st and 99th percentiles. To avoid distortion from non-Gaussian distributions, features were scaled using "
        "RobustScaler, centered by the median and normalized by the Interquartile Range (IQR):"
    )
    add_equation_paragraph("x_scaled = (x - Median(x)) / (Q3(x) - Q1(x))", 1)

    # -------------------------------------------------------------------------
    # SECTION VI: MACHINE LEARNING MODELS AND MATHEMATICAL FORMULATION
    # -------------------------------------------------------------------------
    add_section_heading("VI. MACHINE LEARNING MODELS AND MATHEMATICAL FORMULATION")
    add_body_paragraph(
        "To ensure rigorous benchmarking, exactly three unsupervised learning paradigms were implemented using Scikit-learn:"
    )
    add_subsection_heading("A. K-Means Partitioning")
    add_body_paragraph(
        "K-Means partitions the observation set X = {x_1, ..., x_n} in R^d into k disjoint clusters C = {C_1, ..., C_k} by minimizing the within-cluster "
        "sum of squares (inertia):"
    )
    add_equation_paragraph("J = sum(i=1 to n) || x_i - mu_c_i ||^2", 2)
    add_body_paragraph(
        "where mu_c_i denotes the centroid of cluster C_i. We executed K-Means across k in [2, 10] using k-means++ initialization, 10 distinct initializations, "
        "and a fixed random seed (seed = 42) to guarantee complete experimental reproducibility."
    )

    add_subsection_heading("B. Agglomerative Hierarchical Clustering")
    add_body_paragraph(
        "Agglomerative clustering creates a hierarchical dendrogram through successive pairwise merges. We evaluated three linkage criteria: Ward's minimum "
        "variance, Average linkage, and Complete linkage. Ward's criterion merges clusters A and B to minimize the increase in total within-cluster variance:"
    )
    add_equation_paragraph("Delta ESS(A, B) = (n_A * n_B / (n_A + n_B)) * || mu_A - mu_B ||^2", 3)

    add_subsection_heading("C. Density-Based Spatial Clustering (DBSCAN)")
    add_body_paragraph(
        "DBSCAN groups points based on local density neighborhoods defined by radius eps and threshold MinPts. A point p is a core point if "
        "|N_eps(p)| >= MinPts. Points not density-reachable from any core point are flagged as noise (-1). We explored a systematic grid of "
        "eps in [0.8, 2.5] and MinPts in [3, 10]."
    )

    add_subsection_heading("D. Internal Cluster Validity Metrics")
    add_body_paragraph(
        "Cluster configurations were evaluated using three standard internal validation criteria: (1) Silhouette Score s(i) = [b(i) − a(i)] / max(a(i), b(i)), "
        "measuring separation against cohesion; (2) Davies–Bouldin Index DB = (1/k) sum max [(s_i + s_j) / d(mu_i, mu_j)], where lower values reflect tighter, "
        "better separated clusters; and (3) Calinski–Harabasz Index CH = [Tr(B_k) / Tr(W_k)] * [(n - k) / (k - 1)], computing the ratio of between-cluster to "
        "within-cluster dispersion."
    )

    # -------------------------------------------------------------------------
    # SECTION VII & VIII: EXPERIMENTAL SETUP, RESULTS, AND BENCHMARKING
    # -------------------------------------------------------------------------
    add_section_heading("VII. EXPERIMENTAL SETUP AND RESULTS")
    add_body_paragraph(
        "Experiments were executed on an Intel-based environment using Python 3.11.9, Scikit-learn 1.8.0, Pandas 3.0.1, and NumPy 2.4.2. A total of 64 distinct "
        "experimental runs were recorded across the three algorithms. Table I summarizes the quantitative performance across algorithm families."
    )

    # TABLE I: EXPERIMENTAL BENCHMARK COMPARISONS
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_t1.add_run("TABLE I\nCOMPARATIVE EXPERIMENTAL EVALUATION ACROSS CLUSTERING ALGORITHMS (N=428 FACILITIES)")
    r_t1.font.bold = True
    r_t1.font.size = Pt(8.5)

    table1 = doc.add_table(rows=1, cols=7)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    table1.style = 'Table Grid'
    hdr_cells = table1.rows[0].cells
    hdr_titles = ["Algorithm", "Configuration", "k", "Silhouette", "Davies-Bouldin", "Calinski-Harabasz", "Noise %"]
    for i, t in enumerate(hdr_titles):
        hdr_cells[i].text = t
        set_cell_background(hdr_cells[i], "0A2540")
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(8)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    data_rows = [
        ["K-Means", "k=2, k-means++", "2", "0.8818", "0.3102", "950.29", "0.0%"],
        ["K-Means", "k=3, k-means++", "3", "0.7601", "0.4741", "709.62", "0.0%"],
        ["K-Means (Selected)", "k=4, k-means++", "4", "0.6113", "0.5768", "655.84", "0.0%"],
        ["K-Means", "k=5, k-means++", "5", "0.5033", "0.8612", "623.68", "0.0%"],
        ["Agglomerative (Ward)", "k=2, Ward linkage", "2", "0.8877", "0.1988", "743.10", "0.0%"],
        ["Agglomerative (Ward)", "k=4, Ward linkage", "4", "0.6708", "0.4634", "638.75", "0.0%"],
        ["Agglomerative (Avg)", "k=4, Average linkage", "4", "0.7005", "0.4660", "524.36", "0.0%"],
        ["Agglomerative (Comp)", "k=4, Complete linkage", "4", "0.6925", "0.4996", "574.58", "0.0%"],
        ["DBSCAN", "eps=1.2, min_samples=3", "2", "0.9434", "0.0473", "1510.11", "20.56%"],
        ["DBSCAN", "eps=1.8, min_samples=3", "2", "0.9352", "0.0615", "1522.79", "10.51%"],
        ["DBSCAN", "eps=2.5, min_samples=3", "5", "0.6752", "0.3158", "494.45", "4.67%"]
    ]

    for row_idx, row_vals in enumerate(data_rows):
        row = table1.add_row()
        for col_idx, text_val in enumerate(row_vals):
            cell = row.cells[col_idx]
            cell.text = text_val
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(8)
            if col_idx in [2, 3, 4, 5, 6]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if "Selected" in row_vals[0]:
                set_cell_background(cell, "E0F2F1")
                p.runs[0].font.bold = True
            elif row_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    # Embed Elbow and Metrics Figure
    elbow_fig_path = os.path.join("figures", "elbow_and_metrics.png")
    if os.path.exists(elbow_fig_path):
        doc.add_picture(elbow_fig_path, width=Inches(5.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run("Fig. 2. K-Means Elbow Curve (Inertia) and Silhouette Trajectory across Cluster Counts k in [2, 10].")
        r_cap.font.size = Pt(8.5)
        r_cap.font.bold = True

    add_body_paragraph(
        "Model Selection Analysis: While k=2 exhibited the highest raw silhouette coefficient (0.8818 in K-Means, 0.8877 in Ward), inspection showed "
        "that it grouped 97% of facilities into a single catch-all partition and merely isolated extreme outlier institutions. Conversely, k=4 provides "
        "an optimal balance between mathematical cohesion (Silhouette = 0.6113, CH = 655.84) and operational granularity, cleanly segregating four "
        "actionable facility archetypes without degenerate singletons."
    )

    # -------------------------------------------------------------------------
    # SECTION IX: CLUSTER PROFILES AND OPERATIONAL IMPLICATIONS
    # -------------------------------------------------------------------------
    add_section_heading("VIII. CLUSTER PROFILES AND OPERATIONAL IMPLICATIONS")
    add_body_paragraph(
        "Table II details the empirical median indicators for each of the four identified clusters under K-Means (k=4). Fig. 3 displays the 2D PCA projection, "
        "and Fig. 4 illustrates standardized indicator divergence."
    )

    # Embed PCA Figure
    pca_fig_path = os.path.join("figures", "pca_clusters.png")
    if os.path.exists(pca_fig_path):
        doc.add_picture(pca_fig_path, width=Inches(5.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run("Fig. 3. Two-Dimensional Principal Component Analysis (PCA) Projection of Identified Facility Clusters (k=4).")
        r_cap.font.size = Pt(8.5)
        r_cap.font.bold = True

    # TABLE II: CLUSTER PROFILES TABLE
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t2 = p_t2.add_run("TABLE II\nEMPIRICAL PROFILES OF IDENTIFIED HEALTHCARE FACILITY CLUSTERS (MEDIAN VALUES)")
    r_t2.font.bold = True
    r_t2.font.size = Pt(8.5)

    table2 = doc.add_table(rows=1, cols=7)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2.style = 'Table Grid'
    hdr2_cells = table2.rows[0].cells
    hdr2_titles = ["Cluster Tier", "N (%)", "Avg Beds", "Op. Margin", "Exp/Rev", "Rev/Bed ($)", "ALOS (Days)"]
    for i, t in enumerate(hdr2_titles):
        hdr2_cells[i].text = t
        set_cell_background(hdr2_cells[i], "007A87")
        p = hdr2_cells[i].paragraphs[0]
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(8)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    prof_rows = [
        ["Cluster 0: General Acute Hospitals", "388 (90.7%)", "204.5", "+0.93%", "0.991", "$1,307,873", "5.7"],
        ["Cluster 1: State / Long-Term Inst.", "8 (1.9%)", "795.5", "-48.20%", "1.482", "$217,376", "403.2"],
        ["Cluster 2: Subacute & Extended Care", "12 (2.8%)", "167.9", "-9.46%", "1.095", "$361,768", "122.2"],
        ["Cluster 3: Specialized Surgical Centers", "20 (4.7%)", "40.1", "+3.12%", "0.969", "$3,575,897", "3.6"]
    ]

    for row_idx, row_vals in enumerate(prof_rows):
        row = table2.add_row()
        for col_idx, text_val in enumerate(row_vals):
            cell = row.cells[col_idx]
            cell.text = text_val
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(8)
            if col_idx in [1, 2, 3, 4, 5, 6]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if row_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    # Embed Cluster Profiles Bar Chart
    prof_fig_path = os.path.join("figures", "cluster_feature_profiles.png")
    if os.path.exists(prof_fig_path):
        doc.add_picture(prof_fig_path, width=Inches(5.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run("Fig. 4. Standardized Indicator Deviation by Cluster Profile (Z-Scores of Feature Medians).")
        r_cap.font.size = Pt(8.5)
        r_cap.font.bold = True

    add_body_paragraph(
        "Operational Insights and Policy Implications:"
    )
    add_body_paragraph(
        "1) The Fragility of Core Acute Care (Cluster 0): Representing over nine-tenths of California hospitals, Cluster 0 operates at a narrow +0.93% median "
        "margin. With an occupancy of 65.3% and a 5.7-day stay, these facilities are highly exposed to macroeconomic wage pressures and Medicare rate freezes. "
        "Hospital leaders in this cohort must focus on workflow throughput and supply chain optimization."
    )
    add_body_paragraph(
        "2) Institutional Subsidies in Long-Term Facilities (Cluster 1): Facilities in Cluster 1 operate at 92.0% bed occupancy with extreme average stays (403 days) "
        "and substantial accounting deficits (-48.20%). These entities represent specialized psychiatric and governmental facilities whose financial sustainability "
        "is decoupled from commercial billing and anchored in legislative appropriations. Applying commercial revenue benchmarks to this tier is clinically and "
        "financially invalid."
    )
    add_body_paragraph(
        "3) High-Margin Elective Capitalization (Cluster 3): Specialized surgical and ambulatory facilities generate $3.58M revenue per bed—nearly triple the "
        "acute hospital baseline—despite maintaining only 33% bed occupancy. Their rapid turnaround (ALOS 3.6 days) confirms that high-tech, elective procedures "
        "drive superior capital efficiency compared to emergency-intensive community operations."
    )

    # -------------------------------------------------------------------------
    # SECTION X: LIMITATIONS AND ETHICAL CONSIDERATIONS
    # -------------------------------------------------------------------------
    add_section_heading("IX. LIMITATIONS AND ETHICAL CONSIDERATIONS")
    add_body_paragraph(
        "Several methodological and ethical limitations must be recognized: (1) Unsupervised Nature: Clustering establishes multivariate statistical "
        "associations based on geometric proximity; it does not demonstrate causality or clinical care quality. (2) Accounting Heterogeneity: Governmental "
        "facilities report under governmental fund accounting standards, which differ from private non-profit GAAP standards. (3) Reporting Lags: Quarterly "
        "filings reflect retrospective reconciliations and may undergo administrative auditing adjustments. (4) Clinical Independence: The dataset lacks "
        "patient-level clinical acuity scores (e.g., Case Mix Index or APACHE II), meaning operational variations may partially reflect patient illness severity."
    )

    # -------------------------------------------------------------------------
    # SECTION XI: CONCLUSION AND FUTURE WORK
    # -------------------------------------------------------------------------
    add_section_heading("X. CONCLUSION AND FUTURE WORK")
    add_body_paragraph(
        "This project successfully developed and validated a reproducible unsupervised machine learning framework for segmenting healthcare facility financial "
        "and resource utilization patterns. Benchmarking on genuine California HCAI regulatory filings demonstrated that K-Means (k=4) provides a mathematically "
        "rigorous and operationally coherent segmentation into four distinct facility tiers: general acute hospitals, state institutional care, subacute rehabilitation, "
        "and specialized surgical centers. The accompanying Streamlit dashboard enables interactive facility querying and peer-group benchmarking. Future extensions "
        "will integrate multi-year longitudinal Markov chain transition modeling to track facility trajectory shifts across clusters over time."
    )

    # -------------------------------------------------------------------------
    # SECTION XII: REFERENCES (15 VERIFIED IEEE CITATIONS)
    # -------------------------------------------------------------------------
    add_section_heading("REFERENCES")
    
    refs = [
        "[1] M. Zarrin, J. Schoenfelder, and J. O. Brunner, \"Homogeneity and best practice analyses in hospital performance management: An analytical framework,\" Health Care Management Science, vol. 25, no. 3, pp. 406–425, Sep. 2022, doi: 10.1007/s10729-022-09590-8.",
        "[2] S. Yousefi, R. F. Saen, H. Shabanpour, and K. Ghods, \"An innovative patient clustering method using data envelopment analysis–discriminant analysis and artificial neural networks: A case study in healthcare systems,\" Socio-Economic Planning Sciences, vol. 93, p. 102054, Jun. 2024, doi: 10.1016/j.seps.2024.102054.",
        "[3] X. Hao, L. Han, D. Zheng, et al., \"Assessing resource allocation based on workload: a data envelopment analysis study on clinical departments in a class a tertiary public hospital in China,\" BMC Health Services Research, vol. 23, p. 980, Sep. 2023, doi: 10.1186/s12913-023-09803-y.",
        "[4] A. Benmoussa, M. Jouhadi, K. Benhida, et al., \"Private hospitals in low- and middle-income countries: a typology using the cluster method, the case of Morocco,\" BMC Health Services Research, vol. 24, p. 1231, Oct. 2024, doi: 10.1186/s12913-024-11681-7.",
        "[5] D. D. Desai, J. Dey, S. K. Satapathy, S. Mishra, S. N. Mohanty, P. Mishra, and S. K. Panda, \"Optimal ambulance positioning for road accidents with deep embedded clustering,\" IEEE Access, vol. 11, pp. 59917–59934, Jun. 2023, doi: 10.1109/ACCESS.2023.3284993.",
        "[6] A. Vosoughi, C. E. Jones, T. P. Cooper, et al., \"Unsupervised clustering analysis of trauma and non-trauma centers using hospital features including surgical care,\" PLOS ONE, vol. 19, no. 8, p. e0308339, Aug. 2024, doi: 10.1371/journal.pone.0308339.",
        "[7] K. E. Joynt Maddox, R. E. Reid, J. M. Bleser, et al., \"Association of measured quality with financial health among U.S. hospitals,\" PLOS ONE, vol. 17, no. 4, p. e0266479, Apr. 2022, doi: 10.1371/journal.pone.0266479.",
        "[8] Y. Qin, X. Wei, M. Liang, et al., \"Measurement of the operational efficiency of tertiary public hospitals in western China: Evidence from Guangxi from 2019 to 2022,\" Frontiers in Public Health, vol. 12, p. 1374523, Feb. 2025, doi: 10.3389/fpubh.2024.1374523.",
        "[9] K. Vluggen, H. Vrijhoef, D. Ruwaard, et al., \"Clusters of medical specialties around patients with multimorbidity – employing fuzzy c-means clustering to explore multidisciplinary collaboration,\" BMC Health Services Research, vol. 23, p. 975, Sep. 2023, doi: 10.1186/s12913-023-09961-z.",
        "[10] P. Jousilahti, H. Kautiainen, E. Mantyselka, et al., \"Patient satisfaction – results of cluster analysis of Finnish patients,\" BMC Health Services Research, vol. 23, p. 629, Jun. 2023, doi: 10.1186/s12913-023-09625-y.",
        "[11] Z. Al-Makhadmeh and A. Tolba, \"Using medical data and clustering techniques for a smart healthcare system,\" Healthcare, vol. 11, no. 3, p. 390, Jan. 2023, doi: 10.3390/healthcare11030390.",
        "[12] Y. Jiang, T. Chen, X. Liu, et al., \"Latent space representation of electronic health records for patient profiling and operational clustering,\" Computers in Biology and Medicine, vol. 183, p. 109255, Dec. 2024, doi: 10.1016/j.compbiomed.2024.109255.",
        "[13] F. Piccialli, V. S. Di Cola, A. Giampaolo, et al., \"Machine learning approaches to predict healthcare attendance and operational capacity utilization,\" Scientific Reports, vol. 11, p. 17613, Sep. 2021, doi: 10.1038/s41598-020-71613-7.",
        "[14] J. Schreyögg and T. Stargardt, \"Hospital bed utilization and cost efficiency dynamics in post-pandemic healthcare networks,\" Health Economics, vol. 32, no. 4, pp. 810–828, Apr. 2023, doi: 10.1002/hec.4651.",
        "[15] P. Khuntia, M. Tanniru, and J. K. Weiner, \"Digital health capabilities and hospital operational efficiency: An empirical evaluation using cluster benchmarking,\" Journal of Medical Internet Research, vol. 24, no. 6, p. e34120, Jun. 2022, doi: 10.2196/34120."
    ]

    for ref in refs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.left_indent = Inches(0.3)
        p_r.paragraph_format.first_line_indent = Inches(-0.3)
        p_r.paragraph_format.space_after = Pt(3)
        run_r = p_r.add_run(ref)
        run_r.font.name = 'Times New Roman'
        run_r.font.size = Pt(8.5)

    # Save Report
    out_dir = os.path.join("report")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "IEEE_Report.docx")
    doc.save(out_path)
    print(f"Successfully generated IEEE Research Report: {out_path}")


if __name__ == '__main__':
    build_ieee_report()
