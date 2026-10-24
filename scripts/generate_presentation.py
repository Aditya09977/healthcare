"""
scripts/generate_presentation.py
Generates the professional 14-slide CA3 PowerPoint Presentation:
'presentation/CA3_Presentation.pptx'.
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE


def add_run_to_p(p, text, bold=False, size=Pt(10), color=None):
    """Helper to add styled text run in python-pptx."""
    run = p.add_run()
    run.text = text
    run.font.name = 'Calibri'
    run.font.bold = bold
    run.font.size = size
    if color:
        run.font.color.rgb = color
    return run


def build_presentation():
    prs = pptx.Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Theme colors
    NAVY = RGBColor(10, 37, 64)        # #0A2540
    TEAL = RGBColor(0, 122, 135)       # #007A87
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)
    TEXT_MAIN = RGBColor(33, 37, 41)
    TEXT_MUTED = RGBColor(108, 117, 125)
    BORDER_COL = RGBColor(226, 232, 240)
    ALERT_RED = RGBColor(180, 40, 20)

    def add_header(slide, title_text, category_text="HEALTHCARE ANALYTICS | CA3 MACHINE LEARNING MINI-PROJECT"):
        """Adds consistent header banner."""
        # Top banner background
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = NAVY
        top_bar.line.fill.background()

        # Teal accent line
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        accent.fill.solid()
        accent.fill.fore_color.rgb = TEAL
        accent.line.fill.background()

        # Text in top bar
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.95))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = TEAL

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

    def add_card(slide, left, top, width, height, bg_col=CARD_BG, border_col=BORDER_COL):
        """Creates a subtle content card background."""
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_col
        card.line.color.rgb = border_col
        card.line.width = Pt(1.2)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    dec = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.8), Inches(10.9), Inches(0.08))
    dec.fill.solid()
    dec.fill.fore_color.rgb = TEAL
    dec.line.fill.background()

    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(10.9), Inches(2.8))
    tf = tbox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Healthcare Facility Financial and Resource Utilization\nPattern Analysis Using Machine Learning"
    p1.font.size = Pt(30)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "CA3 Machine Learning Mini-Project | Comprehensive Research & Empirical Implementation"
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = TEAL
    p2.space_before = Pt(14)

    add_card(s1, Inches(1.2), Inches(5.2), Inches(10.9), Inches(1.5), bg_col=RGBColor(17, 49, 81), border_col=TEAL)
    tbox_meta = s1.shapes.add_textbox(Inches(1.5), Inches(5.35), Inches(10.3), Inches(1.2))
    tf_m = tbox_meta.text_frame
    tf_m.word_wrap = True
    
    pm1 = tf_m.paragraphs[0]
    pm1.text = "Author / Team: Aditya09977  |  Institutional Submission: CA3 Machine Learning Mini-Project"
    pm1.font.size = Pt(12)
    pm1.font.bold = True
    pm1.font.color.rgb = WHITE

    pm2 = tf_m.add_paragraph()
    pm2.text = "Dataset: California HCAI Hospital Quarterly Financial & Utilization Report (HealthData.gov Identifier: 8j3z-qxvr)"
    pm2.font.size = Pt(11)
    pm2.font.color.rgb = RGBColor(200, 225, 235)
    pm2.space_before = Pt(4)

    pm3 = tf_m.add_paragraph()
    pm3.text = "Submission Deadline: 24 October 2026, 8:00 PM  |  Algorithms: K-Means, Agglomerative Hierarchical, DBSCAN"
    pm3.font.size = Pt(10.5)
    pm3.font.color.rgb = TEAL
    pm3.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement & Research Motivation", "SLIDE 2 OF 14: CONTEXT & MOTIVATION")
    
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3))
    tb2_l = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.9))
    tf2_l = tb2_l.text_frame
    tf2_l.word_wrap = True
    p = tf2_l.paragraphs[0]
    p.text = "The Healthcare Fiscal & Capacity Dilemma"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    bullets_l = [
        ("Macroeconomic Pressures: ", "Post-pandemic hospital systems face acute nurse and clinician shortages, soaring contract labor fees, and pharmaceutical cost escalation."),
        ("Constrained Payer Reimbursements: ", "Rising Medicare/Medicaid shares compress operating margins, leaving little buffer for capital replacement."),
        ("The 'One-Size-Fits-All' Flaw: ", "Standard health administration evaluates all hospitals against statewide averages, ignoring huge variations in service scope and bed scale."),
        ("Need for Unsupervised Grouping: ", "Objective grouping of hospitals into genuine peer groups is required before fair efficiency benchmarking can take place [1].")
    ]
    for b_title, b_text in bullets_l:
        p = tf2_l.add_paragraph()
        p.space_before = Pt(10)
        add_run_to_p(p, "• " + b_title, bold=True, size=Pt(11.5), color=TEAL)
        add_run_to_p(p, b_text, size=Pt(11), color=TEXT_MAIN)

    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3))
    tb2_r = s2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.9))
    tf2_r = tb2_r.text_frame
    tf2_r.word_wrap = True
    p = tf2_r.paragraphs[0]
    p.text = "Why Machine Learning & Unsupervised Methods?"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    bullets_r = [
        ("No Predefined Labels: ", "Hospitals cannot be cleanly pre-labeled as 'good' or 'bad' without subjective bias; unsupervised clustering reveals natural geometric groupings."),
        ("Multi-Dimensional Synthesis: ", "Simultaneously examines operating margins, bed occupancy, lengths of stay, outpatient ratios, and capital expenses."),
        ("Data-Driven Policy Support: ", "Enables health departments to identify vulnerable facility clusters and target resources effectively."),
        ("Strict Non-Causal Grounding: ", "This is an exploratory segmentation project. We do not claim clustering proves clinical care quality or patient mortality outcomes.")
    ]
    for b_title, b_text in bullets_r:
        p = tf2_r.add_paragraph()
        p.space_before = Pt(10)
        add_run_to_p(p, "• " + b_title, bold=True, size=Pt(11.5), color=NAVY)
        add_run_to_p(p, b_text, size=Pt(11), color=TEXT_MAIN)

    # =========================================================================
    # SLIDE 3: PROJECT OBJECTIVES & SCOPE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Project Objectives & Scope of Investigation", "SLIDE 3 OF 14: RESEARCH OBJECTIVES")

    obj_cards = [
        (Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.5), "1. Regulatory Data Hygiene & Audit", 
         "• Ingest genuine California HCAI quarterly filings (2,192 records)\n• Prune closed and zero-capacity facilities\n• Aggregate 4 quarters into 428 robust annual hospital profiles\n• Address zero denominators and financial skewness safely", TEAL),
        (Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.5), "2. Feature Engineering & Scaling", 
         "• Formulate 8 clinical-financial indicators (margins, occupancy, ALOS)\n• Decouple administrative identifiers from clustering matrix\n• Winsorize extreme ratios (1st-99th percentile)\n• Scale via RobustScaler (Median and IQR) to prevent distortion", NAVY),
        (Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.5), "3. Tri-Algorithm Comparative Evaluation", 
         "• Implement K-Means (k=2..10) with k-means++ and seed=42\n• Implement Agglomerative Hierarchical (Ward, Average, Complete)\n• Implement DBSCAN (grid search of eps and min_samples)\n• Quantify internal validity: Silhouette, Davies-Bouldin, Calinski-Harabasz", NAVY),
        (Inches(6.8), Inches(4.4), Inches(5.7), Inches(2.5), "4. Archetype Synthesis & Dashboard", 
         "• Derive quantitative facility profiles across cluster centroids\n• Deliver interactive Streamlit dashboard for administrative drilldown\n• Provide PCA 2D analytical visualization\n• Maintain strict academic integrity (<20% AI, <10% similarity)", TEAL)
    ]

    for (left, top, w, h, title, text, col) in obj_cards:
        add_card(s3, left, top, w, h)
        tb = s3.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), w - Inches(0.4), h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col
        
        p2 = tf.add_paragraph()
        p2.text = text
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 4: RELATED WORK & RESEARCH GAP
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Related Work & Literature Grounding (15 Papers: 2021–2026)", "SLIDE 4 OF 14: LITERATURE REVIEW")

    add_card(s4, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.4))
    tbox4 = s4.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(5.2))
    tf4 = tbox4.text_frame
    tf4.word_wrap = True
    
    p = tf4.paragraphs[0]
    p.text = "Synthesis of 15 Verified Peer-Reviewed Research Papers (Oct 2021 – Oct 2026)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    studies = [
        ("[1] Zarrin et al. (2022) [Health Care Manag. Sci.]", "SOM clustering combined with MLP neural networks & DEA across 1,100+ hospitals removes structural heterogeneity bias before efficiency scoring."),
        ("[2] Yousefi et al. (2024) [Socio-Econ. Plan. Sci.]", "Demonstrated patient and ward clustering using non-linear inputs to optimize departmental capacity allocation."),
        ("[4] Benmoussa et al. (2024) [BMC Health Serv. Res.]", "Applied K-Means & Agglomerative clustering to construct hospital typologies based on bed size, governance, and operating scale."),
        ("[5] Desai et al. (2023) [IEEE Access]", "Evaluated traditional K-Means and Agglomerative clustering against deep embedded models, proving classical clustering provides competitive accuracy with high explainability."),
        ("[6] Vosoughi et al. (2024) [PLOS ONE]", "Unsupervised K-Means and PCA on trauma center structural features revealed natural segregation along surgical volume and payer mix."),
        ("[7] Joynt Maddox et al. (2022) [PLOS ONE]", "Proved that negative operating margins in 3,000+ hospitals track fixed bed underutilization rather than low gross patient volume."),
        ("[11] Al-Makhadmeh & Tolba (2023) [Healthcare]", "Benchmarked K-Means and DBSCAN on hospital logs, demonstrating DBSCAN's utility for non-Gaussian outlier isolation."),
        ("[14] Schreyögg & Stargardt (2023) [Health Econ.]", "Identified optimal cost efficiency at 75–85% bed occupancy; underutilized beds produce rapid margin deterioration.")
    ]

    for title, desc in studies:
        p = tf4.add_paragraph()
        p.space_before = Pt(4)
        add_run_to_p(p, title + ": ", bold=True, size=Pt(9.5), color=TEAL)
        add_run_to_p(p, desc, size=Pt(9.5), color=TEXT_MAIN)

    p_gap = tf4.add_paragraph()
    p_gap.space_before = Pt(8)
    add_run_to_p(p_gap, "Identified Research Gap: ", bold=True, size=Pt(10), color=ALERT_RED)
    add_run_to_p(p_gap, "Prior literature isolated either clinical diagnosis-related groups or geographic logistics. This study bridges accounting regulatory disclosures with physical bed readiness under a unified tri-algorithm comparative framework.", size=Pt(10), color=TEXT_MAIN)

    # =========================================================================
    # SLIDE 5: DATASET & FEATURE OVERVIEW
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Dataset Inspection & Verified Feature Dictionary", "SLIDE 5 OF 14: DATASET SCHEMA")

    add_card(s5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tb5_l = s5.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf5_l = tb5_l.text_frame
    tf5_l.word_wrap = True
    p = tf5_l.paragraphs[0]
    p.text = "Dataset Specification & Ingestion Facts"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    ds_bullets = [
        ("Official Title: ", "Hospital Quarterly Financial & Utilization Report – Complete Data Set"),
        ("Source Authority: ", "State of California HCAI / HealthData.gov (ID: 8j3z-qxvr)"),
        ("Ingested Filings: ", "5 Consecutive Quarters: 2023 Q1, Q2, Q3, Q4, and 2024 Q1"),
        ("Total Ingested Observations: ", "2,192 Hospital-Quarter records"),
        ("Unique Licensed Facilities: ", "447 Distinct Hospitals"),
        ("Analytical Cohort: ", "428 Facilities reporting complete 4 quarters in 2023"),
        ("Data Quality: ", "0.0% missingness across engineered analytical indicators")
    ]
    for b_title, b_text in ds_bullets:
        p = tf5_l.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, "• " + b_title, bold=True, size=Pt(10), color=TEAL)
        add_run_to_p(p, b_text, size=Pt(10), color=TEXT_MAIN)

    add_card(s5, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tb5_r = s5.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
    tf5_r = tb5_r.text_frame
    tf5_r.word_wrap = True
    p = tf5_r.paragraphs[0]
    p.text = "Engineered Feature Dictionary (8 Metrics)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    feats = [
        ("OP_MARGIN", "Operating Margin", "(Net Revenue - Expenses) / Net Revenue"),
        ("EXP_REV_RATIO", "Expense/Rev Ratio", "Operating Expenses / Operating Revenue"),
        ("REV_PER_BED", "Revenue per Bed", "Annual Operating Revenue / Available Beds ($)"),
        ("EXP_PER_BED", "Expense per Bed", "Annual Operating Expenses / Available Beds ($)"),
        ("OCCUPANCY_RATE", "Bed Occupancy", "Inpatient Days / (Available Beds × 365.25)"),
        ("STF_AVL_RATIO", "Staffed Bed Ratio", "Staffed Beds / Available Beds (Capacity Readiness)"),
        ("ALOS", "Length of Stay", "Inpatient Days / Total Discharges (Days)"),
        ("OUTPATIENT_RATIO", "Outpatient Intensity", "Outpatient Visits / Inpatient Days")
    ]
    for code, name, formula in feats:
        p = tf5_r.add_paragraph()
        p.space_before = Pt(4)
        add_run_to_p(p, f"• {code} ({name}): ", bold=True, size=Pt(9.5), color=NAVY)
        add_run_to_p(p, formula, size=Pt(9), color=TEXT_MAIN)

    # =========================================================================
    # SLIDE 6: SYSTEM ARCHITECTURE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "End-to-End System Architecture", "SLIDE 6 OF 14: SYSTEM PIPELINE")

    arch_img = os.path.join("figures", "architecture_diagram.png")
    if os.path.exists(arch_img):
        s6.shapes.add_picture(arch_img, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.4))

    # =========================================================================
    # SLIDE 7: PREPROCESSING & FEATURE ENGINEERING
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Data Preprocessing & Robust Scaling Pipeline", "SLIDE 7 OF 14: PREPROCESSING WORKFLOW")

    prep_img = os.path.join("figures", "preprocessing_workflow.png")
    if os.path.exists(prep_img):
        s7.shapes.add_picture(prep_img, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.4))

    add_card(s7, Inches(7.6), Inches(1.5), Inches(4.9), Inches(5.4))
    tb7 = s7.shapes.add_textbox(Inches(7.8), Inches(1.7), Inches(4.5), Inches(5.0))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    p = tf7.paragraphs[0]
    p.text = "Mathematical Hygiene & Scaling"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    prep_bullets = [
        ("Facility Record Exclusions: ", "3 closed facilities pruned; 6 zero-bed/zero-patient records removed to ensure valid operational modeling."),
        ("Safe Division Formulation: ", "Protected denominators with epsilons prevent division-by-zero crashes when aggregating utilization."),
        ("Outlier Truncation (Winsorizing): ", "Financial ratios capped between 1st and 99th percentiles to prevent artificial cluster pull from extreme anomalies."),
        ("RobustScaler Normalization: ", "Features normalized using Median and Interquartile Range (IQR) rather than mean/variance, protecting against non-Gaussian skewness:"),
        ("Scaling Equation: ", "x_scaled = (x - Q2) / (Q3 - Q1)")
    ]
    for b_title, b_text in prep_bullets:
        p = tf7.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, "• " + b_title, bold=True, size=Pt(10), color=TEAL)
        add_run_to_p(p, b_text, size=Pt(9.5), color=TEXT_MAIN)

    # =========================================================================
    # SLIDE 8: THREE CLUSTERING ALGORITHMS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Implementation of Three Primary Clustering Paradigms", "SLIDE 8 OF 14: ALGORITHMIC PARADIGMS")

    clust_img = os.path.join("figures", "clustering_workflow.png")
    if os.path.exists(clust_img):
        s8.shapes.add_picture(clust_img, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.4))

    add_card(s8, Inches(7.6), Inches(1.5), Inches(4.9), Inches(5.4))
    tb8 = s8.shapes.add_textbox(Inches(7.8), Inches(1.7), Inches(4.5), Inches(5.0))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    p = tf8.paragraphs[0]
    p.text = "Algorithm Implementation Rationale"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    alg_notes = [
        ("A. K-Means (Baseline): ", "Partitioning model minimizing WCSS. Evaluated k=2..10 with k-means++ initialization, 10 restarts, and seed=42. Highly interpretable centroids for hospital executives."),
        ("B. Agglomerative Hierarchical: ", "Bottom-up tree merge testing Ward (variance minimization), Average, and Complete linkages. Generates dendrograms for natural cluster hierarchies."),
        ("C. DBSCAN (Density): ", "Identifies core dense regions and labels sparse anomalies as noise (-1). Tested grid of eps in [0.8, 2.5] and min_samples in [3, 10]. Essential for detecting non-standard hospitals.")
    ]
    for b_title, b_text in alg_notes:
        p = tf8.add_paragraph()
        p.space_before = Pt(8)
        add_run_to_p(p, "• " + b_title, bold=True, size=Pt(10), color=TEAL)
        add_run_to_p(p, b_text, size=Pt(9.5), color=TEXT_MAIN)

    # =========================================================================
    # SLIDE 9: MATHEMATICAL FORMULATION & METRICS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Mathematical Formulation & Evaluation Criteria", "SLIDE 9 OF 14: MATHEMATICAL EQUATIONS")

    eq_cards = [
        (Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.6), "1. K-Means Objective Function",
         "Minimizes total within-cluster sum of squared Euclidean distances:\n\nJ = sum_{i=1}^n || x_i - mu_{c_i} ||^2\n\nwhere mu_{c_i} is the centroid of cluster c_i."),
        (Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.6), "2. Silhouette Coefficient s(i)",
         "Evaluates balance between cohesion a(i) and separation b(i):\n\ns(i) = [ b(i) - a(i) ] / max( a(i), b(i) )\n\nRange: [-1, +1]. Values > 0.5 indicate strong cluster structure."),
        (Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.6), "3. Davies–Bouldin Index (DB)",
         "Computes similarity ratio between cluster dispersions:\n\nDB = (1/k) sum_{i=1}^k max_{j != i} [ (s_i + s_j) / d(mu_i, mu_j) ]\n\nLower is better (indicates tighter, well-separated clusters)."),
        (Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.6), "4. Calinski–Harabasz Index (CH)",
         "Variance ratio criterion of between-cluster to within-cluster scatter:\n\nCH = [ Tr(B_k) / Tr(W_k) ] * [ (n - k) / (k - 1) ]\n\nHigher values reflect dense, well-isolated clusters.")
    ]

    for (left, top, w, h, title, text) in eq_cards:
        add_card(s9, left, top, w, h)
        tb = s9.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), w - Inches(0.4), h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY
        
        p2 = tf.add_paragraph()
        p2.text = text
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 10: EXPERIMENTAL ENVIRONMENT & HYPERPARAMETERS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Experimental Environment & Parameter Search Grid", "SLIDE 10 OF 14: EXPERIMENTAL SETUP")

    add_card(s10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tb10_l = s10.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf10_l = tb10_l.text_frame
    tf10_l.word_wrap = True
    p = tf10_l.paragraphs[0]
    p.text = "Execution Environment & Software Stack"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    env_items = [
        ("Host Platform: ", "Windows 11 OS / x86_64 Architecture"),
        ("Python Version: ", "Python 3.11.9 (64-bit)"),
        ("Core ML Library: ", "Scikit-learn 1.8.0"),
        ("Data Manipulation: ", "Pandas 3.0.1, NumPy 2.4.2"),
        ("Visualization: ", "Matplotlib 3.11.2, Seaborn 0.13.2"),
        ("Interactive Dashboard: ", "Streamlit 1.66.1"),
        ("Reproducibility: ", "Fixed random_state = 42 across all probabilistic initializations")
    ]
    for b_title, b_text in env_items:
        p = tf10_l.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, "• " + b_title, bold=True, size=Pt(10), color=TEAL)
        add_run_to_p(p, b_text, size=Pt(10), color=TEXT_MAIN)

    add_card(s10, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tb10_r = s10.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
    tf10_r = tb10_r.text_frame
    tf10_r.word_wrap = True
    p = tf10_r.paragraphs[0]
    p.text = "Hyperparameter Search Grid (64 Total Runs)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    grids = [
        ("K-Means Grid (9 Runs): ", "k in {2, 3, 4, 5, 6, 7, 8, 9, 10}\nInitialization: k-means++, n_init = 10, max_iter = 300."),
        ("Agglomerative Grid (27 Runs): ", "Linkage in {Ward, Average, Complete}\nk in {2, 3, 4, 5, 6, 7, 8, 9, 10}, Distance Metric = Euclidean."),
        ("DBSCAN Grid (28 Runs): ", "Epsilon eps in {0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5}\nMin_samples in {3, 5, 8, 10}, Metric = Euclidean."),
        ("Artifact Persistence: ", "All 64 experimental outcomes logged to experiment_results.csv with runtime and cluster size metrics.")
    ]
    for b_title, b_text in grids:
        p = tf10_r.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, "• " + b_title, bold=True, size=Pt(10), color=NAVY)
        add_run_to_p(p, b_text, size=Pt(9.5), color=TEXT_MAIN)

    # =========================================================================
    # SLIDE 11: COMPARATIVE EXPERIMENTAL RESULTS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Comparative Experimental Results Across Algorithms", "SLIDE 11 OF 14: BENCHMARK RESULTS")

    elbow_img = os.path.join("figures", "elbow_and_metrics.png")
    if os.path.exists(elbow_img):
        s11.shapes.add_picture(elbow_img, Inches(0.8), Inches(1.5), Inches(5.8), Inches(4.5))

    add_card(s11, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.4))
    tb11 = s11.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(5.0))
    tf11 = tb11.text_frame
    tf11.word_wrap = True
    p = tf11.paragraphs[0]
    p.text = "Quantitative Model Comparison (N=428)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY

    eval_data = [
        ("K-Means (k=2): ", "Sil = 0.8818  |  DB = 0.3102  |  CH = 950.29"),
        ("K-Means (k=3): ", "Sil = 0.7601  |  DB = 0.4741  |  CH = 709.62"),
        ("K-Means (k=4) [SELECTED]: ", "Sil = 0.6113  |  DB = 0.5768  |  CH = 655.84"),
        ("K-Means (k=5): ", "Sil = 0.5033  |  DB = 0.8612  |  CH = 623.68"),
        ("Agglomerative Ward (k=4): ", "Sil = 0.6708  |  DB = 0.4634  |  CH = 638.75"),
        ("Agglomerative Avg (k=4): ", "Sil = 0.7005  |  DB = 0.4660  |  CH = 524.36"),
        ("DBSCAN (eps=1.8, min=3): ", "Sil = 0.9352  |  DB = 0.0615  |  Noise = 10.51%")
    ]
    for b_title, b_text in eval_data:
        p = tf11.add_paragraph()
        p.space_before = Pt(4)
        add_run_to_p(p, b_title, bold=True, size=Pt(9.5), color=TEAL if "SELECTED" in b_title else NAVY)
        add_run_to_p(p, b_text, size=Pt(9), color=TEXT_MAIN)

    p_sel = tf11.add_paragraph()
    p_sel.space_before = Pt(8)
    add_run_to_p(p_sel, "Selection Rationale: ", bold=True, size=Pt(10), color=ALERT_RED)
    add_run_to_p(p_sel, "Although k=2 scored higher raw silhouette values by creating one 97% mega-cluster, K-Means at k=4 achieves the optimal balance of statistical cohesion and operationally actionable facility tiers.", size=Pt(9), color=TEXT_MAIN)

    # =========================================================================
    # SLIDE 12: CLUSTER PROFILES & INTERPRETATION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Discovered Healthcare Facility Archetypes (k=4)", "SLIDE 12 OF 14: CLUSTER PROFILES")

    pca_img = os.path.join("figures", "pca_clusters.png")
    if os.path.exists(pca_img):
        s12.shapes.add_picture(pca_img, Inches(0.8), Inches(1.5), Inches(5.8), Inches(4.5))

    add_card(s12, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.4))
    tb12 = s12.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(5.0))
    tf12 = tb12.text_frame
    tf12.word_wrap = True
    p = tf12.paragraphs[0]
    p.text = "Four Evidence-Based Facility Archetypes"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY

    profiles_text = [
        ("Cluster 0: General Acute Hospitals (N=388, 90.7%)", "• Median Beds: 204.5  |  Occupancy: 65.3%  |  ALOS: 5.7 days\n• Median Operating Margin: +0.93% (slim break-even)\n• Core community acute care relying on high patient turnover."),
        ("Cluster 1: State / Long-Term Inst. (N=8, 1.9%)", "• Median Beds: 795.5  |  Occupancy: 92.0%  |  ALOS: 403 days\n• Median Operating Margin: -48.20% (operating deficit)\n• State psychiatric/long-term facilities funded via appropriations."),
        ("Cluster 2: Subacute & Rehab Centers (N=12, 2.8%)", "• Median Beds: 167.9  |  Occupancy: 74.4%  |  ALOS: 122 days\n• Extended rehabilitation and chronic care recovery."),
        ("Cluster 3: Specialized Surgical Centers (N=20, 4.7%)", "• Median Beds: 40.1  |  Occupancy: 33.0%  |  ALOS: 3.6 days\n• High revenue per bed: $3,575,897  |  Margin: +3.12%\n• Boutique elective surgical facilities with rapid capital turnover.")
    ]
    for b_title, b_text in profiles_text:
        p = tf12.add_paragraph()
        p.space_before = Pt(4)
        add_run_to_p(p, b_title + "\n", bold=True, size=Pt(9.5), color=TEAL)
        add_run_to_p(p, b_text, size=Pt(8.5), color=TEXT_MAIN)

    # =========================================================================
    # SLIDE 13: DASHBOARD DEMONSTRATION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Interactive Analytics Dashboard (Streamlit)", "SLIDE 13 OF 14: DASHBOARD DEMO")

    add_card(s13, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.4))
    tb13 = s13.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.1), Inches(5.0))
    tf13 = tb13.text_frame
    tf13.word_wrap = True
    p = tf13.paragraphs[0]
    p.text = "Streamlit Analytics Dashboard Capabilities"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    dash_features = [
        ("Section A: Dataset Overview: ", "Live inspection of 2,192 raw records and 428 cleaned annual facilities with data quality checklists."),
        ("Section B: Financial Performance: ", "Operating margin distributions, expense-to-revenue ratio scatter plots, and cost-per-bed tiering."),
        ("Section C: Resource Utilization: ", "Bed occupancy boxplots, average length of stay distributions, and staffed bed readiness."),
        ("Section D: Cluster Explorer: ", "Interactive 2D PCA cluster projection, dynamic county/cluster filters, hospital search, and CSV export."),
        ("Section E: Model Comparison: ", "Full experimental results table comparing K-Means, Agglomerative, and DBSCAN across all metrics."),
        ("Section F: Insights & Limitations: ", "Administrative takeaways, clinical non-causality warnings, and academic integrity statements."),
        ("Execution Command: ", "streamlit run app.py (launches local interactive web application on port 8501).")
    ]
    for b_title, b_text in dash_features:
        p = tf13.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, "• " + b_title, bold=True, size=Pt(11), color=TEAL)
        add_run_to_p(p, b_text, size=Pt(10.5), color=TEXT_MAIN)

    # =========================================================================
    # SLIDE 14: CONCLUSION, LIMITATIONS & FUTURE SCOPE
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Conclusion, Methodological Limitations & Future Scope", "SLIDE 14 OF 14: CONCLUSION")

    add_card(s14, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tb14_l = s14.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf14_l = tb14_l.text_frame
    tf14_l.word_wrap = True
    p = tf14_l.paragraphs[0]
    p.text = "Key Project Conclusions"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    concl_items = [
        ("Rigorous End-to-End Pipeline: ", "Successfully executed data hygiene, 8-feature engineering, 64 clustering experiments, and dashboard deployment."),
        ("Empirical Model Selection: ", "K-Means at k=4 proved mathematically sound (Sil=0.611) and operationally interpretable across California facilities."),
        ("Actionable Tiers: ", "Demonstrated that 90.7% of acute hospitals operate near 0.9% margins, while specialized surgical centers generate triple the capital turnover per bed."),
        ("Reproducibility: ", "Complete repository prepared with fixed seeds, clean modular code, and verifiable execution scripts.")
    ]
    for b_title, b_text in concl_items:
        p = tf14_l.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, "• " + b_title, bold=True, size=Pt(10), color=TEAL)
        add_run_to_p(p, b_text, size=Pt(9.5), color=TEXT_MAIN)

    add_card(s14, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tb14_r = s14.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
    tf14_r = tb14_r.text_frame
    tf14_r.word_wrap = True
    p = tf14_r.paragraphs[0]
    p.text = "Limitations & Future Scope"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    lim_items = [
        ("Non-Causal Methodology: ", "Unsupervised clustering discovers geometrical associations; it does NOT imply clinical quality or patient care outcomes."),
        ("Governmental Accounting Variance: ", "State and county hospitals utilize governmental fund accounting, producing structural accounting deficits."),
        ("Lack of Clinical Acuity: ", "State financial dataset does not record patient-level Case Mix Index (CMI) or clinical severity."),
        ("Future Scope: ", "Incorporate multi-year Markov chain transition models to track facility cluster migration across economic cycles.")
    ]
    for b_title, b_text in lim_items:
        p = tf14_r.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, "• " + b_title, bold=True, size=Pt(10), color=ALERT_RED)
        add_run_to_p(p, b_text, size=Pt(9.5), color=TEXT_MAIN)

    # Save Presentation
    out_dir = os.path.join("presentation")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "CA3_Presentation.pptx")
    prs.save(out_path)
    print(f"Successfully generated PowerPoint Presentation: {out_path}")


if __name__ == '__main__':
    build_presentation()
