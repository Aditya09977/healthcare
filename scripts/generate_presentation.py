"""
scripts/generate_presentation.py
Generates an executive-grade 14-slide CA3 PowerPoint Presentation:
'presentation/CA3_Presentation.pptx'.

Features & Design Standards:
- Zero awkward blank spaces: Proportional card layouts, tables, and dense academic content.
- Professional Healthcare Color Palette (Deep Navy #0A2540, Medical Teal #007A87, Clean Slate #F8FAFC, Accent Alert #BE281E).
- Structured Executive Card Panels with dedicated color-coded header bars.
- Real PowerPoint Tables for feature dictionaries, hyperparameter grids, model benchmarks, and cluster profiles.
- Widescreen 16:9 geometry (13.333" x 7.5").
- Complete alignment with IEEE report and CA3 machine learning deliverables.
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR


# =============================================================================
# COLOR PALETTE CONSTANTS
# =============================================================================
NAVY = RGBColor(10, 37, 64)          # #0A2540 - Primary Brand
NAVY_LIGHT = RGBColor(26, 68, 108)    # #1A446C - Secondary Accent
TEAL = RGBColor(0, 122, 135)         # #007A87 - Clinical Teal
TEAL_DARK = RGBColor(0, 85, 95)      # #00555F - Deep Teal
TEAL_LIGHT = RGBColor(230, 246, 248) # #E6F6F8 - Subtle Fill
WHITE = RGBColor(255, 255, 255)
BG_PAGE = RGBColor(245, 247, 250)    # #F5F7FA - Slide Background
CARD_BG = RGBColor(255, 255, 255)    # Card Canvas
CARD_BORDER = RGBColor(205, 215, 225)# Card Border Line
TEXT_DARK = RGBColor(25, 35, 48)     # Primary Body Text
TEXT_MUTED = RGBColor(90, 105, 120)  # Secondary / Captions
ALERT_RED = RGBColor(185, 35, 25)    # Outlier / Fiscal Deficit
SUCCESS_GREEN = RGBColor(20, 115, 60)# High Efficiency / Profitable
GOLD = RGBColor(190, 110, 15)        # Warning / Transitional
ROW_ALT = RGBColor(245, 248, 252)    # Table Alternating Row


def add_run_to_p(p, text, bold=False, size=Pt(10), color=None, italic=False):
    """Helper to add styled text run in python-pptx."""
    run = p.add_run()
    run.text = text
    run.font.name = 'Calibri'
    run.font.bold = bold
    run.font.italic = italic
    run.font.size = size
    if color:
        run.font.color.rgb = color
    return run


def style_cell(cell, text="", bold=False, size=Pt(9), color=TEXT_DARK, 
               bg_color=None, align=PP_ALIGN.LEFT, bold_prefix=None):
    """Formats a table cell with text, alignment, font, and background."""
    if bg_color:
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.08)
    tf.margin_right = Inches(0.08)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    
    p = tf.paragraphs[0]
    p.alignment = align
    if bold_prefix:
        add_run_to_p(p, bold_prefix, bold=True, size=size, color=color)
        add_run_to_p(p, text, bold=bold, size=size, color=color)
    else:
        add_run_to_p(p, text, bold=bold, size=size, color=color)


def create_header(slide, title_text, category_text, slide_num):
    """Creates an executive top header banner and standard footer."""
    # Top navy header
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.05))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = NAVY
    top_bar.line.fill.background()

    # Teal accent rule
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.05), Inches(13.333), Inches(0.05))
    accent.fill.solid()
    accent.fill.fore_color.rgb = TEAL
    accent.line.fill.background()

    # Title box
    txBox = slide.shapes.add_textbox(Inches(0.75), Inches(0.10), Inches(10.8), Inches(0.85))
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(9)
    p_cat.font.bold = True
    p_cat.font.color.rgb = TEAL

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(19)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE

    # Slide number badge
    txNum = slide.shapes.add_textbox(Inches(11.3), Inches(0.22), Inches(1.3), Inches(0.6))
    tf_num = txNum.text_frame
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"{slide_num} / 14"
    p_num.font.size = Pt(13)
    p_num.font.bold = True
    p_num.font.color.rgb = WHITE

    # Footer
    txFoot = slide.shapes.add_textbox(Inches(0.75), Inches(7.18), Inches(11.83), Inches(0.28))
    tf_foot = txFoot.text_frame
    tf_foot.margin_top = tf_foot.margin_bottom = tf_foot.margin_left = tf_foot.margin_right = 0
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = "CA3 Machine Learning Mini-Project  |  Healthcare Facility Analytics  |  Candidate: Aditya09977  |  Submission: Oct 2026"
    p_foot.font.size = Pt(8.5)
    p_foot.font.color.rgb = TEXT_MUTED


def add_card_panel(slide, left, top, width, height, header_text="", header_color=NAVY, 
                   header_height=Inches(0.36), bg_color=CARD_BG, border_color=CARD_BORDER):
    """
    Creates a professional structured card with an optional colored top header strip.
    Returns (body_textbox, text_frame) positioned neatly within the card body.
    """
    # Base card rectangle
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.0)

    if header_text:
        # Header banner strip
        hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, header_height)
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = header_color
        hdr.line.fill.background()

        # Header title
        tb_h = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.04), width - Inches(0.3), header_height - Inches(0.08))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        tf_h.margin_top = tf_h.margin_bottom = tf_h.margin_left = tf_h.margin_right = 0
        p_h = tf_h.paragraphs[0]
        p_h.text = header_text
        p_h.font.size = Pt(10.5)
        p_h.font.bold = True
        p_h.font.color.rgb = WHITE

        # Body text box
        body_top = top + header_height + Inches(0.08)
        body_height = height - header_height - Inches(0.14)
        body_left = left + Inches(0.16)
        body_width = width - Inches(0.32)

        tb_b = slide.shapes.add_textbox(body_left, body_top, body_width, body_height)
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_top = tf_b.margin_bottom = tf_b.margin_left = tf_b.margin_right = 0
        return tb_b, tf_b
    else:
        body_top = top + Inches(0.10)
        body_height = height - Inches(0.20)
        body_left = left + Inches(0.16)
        body_width = width - Inches(0.32)

        tb_b = slide.shapes.add_textbox(body_left, body_top, body_width, body_height)
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_top = tf_b.margin_bottom = tf_b.margin_left = tf_b.margin_right = 0
        return tb_b, tf_b


def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_canvas_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_PAGE
        bg.line.fill.background()
        return bg

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Balanced Hero + 4 Metadata Callouts)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Top Department Badge
    dep_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.4))
    tf_dep = dep_box.text_frame
    p_dep = tf_dep.paragraphs[0]
    p_dep.text = "ACADEMIC YEAR 2026-2027  |  DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
    p_dep.font.size = Pt(11)
    p_dep.font.bold = True
    p_dep.font.color.rgb = TEAL

    # Teal divider
    s1_rule = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.733), Inches(0.05))
    s1_rule.fill.solid()
    s1_rule.fill.fore_color.rgb = TEAL
    s1_rule.line.fill.background()

    # Title & Subtitle Frame
    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.733), Inches(2.7))
    tf = tbox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Healthcare Facility Financial and Resource Utilization\nPattern Analysis Using Machine Learning"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "CA3 Machine Learning Mini-Project  |  Tri-Algorithm Clustering, Empirical Benchmarking & Decision Support"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = TEAL
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "Rigorous unsupervised partitioning of 428 California healthcare facilities from multi-quarter state disclosures."
    p3.font.size = Pt(11)
    p3.font.color.rgb = RGBColor(190, 205, 220)
    p3.space_before = Pt(6)

    # 4 Bottom KPI / Metadata Cards (Filling Y=4.6 to 6.85, height 2.25")
    s1_cards = [
        ("PRIMARY DATASET", "California HCAI / HealthData.gov", "5 Quarters (2023 Q1-Q4, 2024 Q1)\n2,192 Raw Filings  |  428 Clean Cohort\nZero Missingness (0.0% Imputation)\nFull Audited Balance Sheet Data", Inches(0.8)),
        ("MACHINE LEARNING", "Tri-Algorithm Suite (64 Runs)", "K-Means (k=4 Selected Solution)\nAgglomerative (Ward, Avg, Complete)\nDBSCAN Density Anomaly Search\nComprehensive Metric Evaluation", Inches(3.78)),
        ("ACADEMIC RIGOR", "IEEE 6-Page Conference Paper", "15 Verified Papers (Oct 2021-2026)\n<10% Plagiarism  |  <20% AI Index\nMathematical Validation (Sil, DB, CH)\nNon-Causal Academic Framing", Inches(6.76)),
        ("SUBMISSION DETAILS", "Candidate: Aditya09977", "Course: CA3 Machine Learning\nTarget Deadline: 24 Oct 2026, 8:00 PM\nLive Streamlit Interactive App\nComplete Reproducible GitHub Repo", Inches(9.74))
    ]
    for cat, heading, body, left_pos in s1_cards:
        panel = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, Inches(4.55), Inches(2.78), Inches(2.25))
        panel.fill.solid()
        panel.fill.fore_color.rgb = RGBColor(16, 48, 80)
        panel.line.color.rgb = TEAL
        panel.line.width = Pt(1.2)

        tb_p = s1.shapes.add_textbox(left_pos + Inches(0.15), Inches(4.65), Inches(2.48), Inches(2.05))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True
        
        p_c = tf_p.paragraphs[0]
        p_c.text = cat
        p_c.font.size = Pt(9)
        p_c.font.bold = True
        p_c.font.color.rgb = TEAL

        p_h = tf_p.add_paragraph()
        p_h.text = heading
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = WHITE
        p_h.space_before = Pt(3)

        p_b = tf_p.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = RGBColor(210, 225, 240)
        p_b.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION (Dense 2-Column x 2-Row Grid)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s2)
    create_header(s2, "Problem Statement & Operational Context", "CONTEXT & MOTIVATION", 2)

    # Top-Left: Macro Economic Pressures
    _, tf_tl = add_card_panel(s2, Inches(0.75), Inches(1.25), Inches(5.75), Inches(2.75), 
                              "1. Post-Pandemic Healthcare Fiscal Pressures", NAVY)
    p = tf_tl.paragraphs[0]
    add_run_to_p(p, "• Acute Labor Shortages & Wage Inflation: ", bold=True, size=Pt(10), color=NAVY)
    add_run_to_p(p, "Hospitals confront escalating staffing expenses driven by traveling nurse premiums and clinical overtime, compressing operating margins across general acute facilities [1], [7].\n", size=Pt(9.5), color=TEXT_DARK)
    
    p = tf_tl.add_paragraph()
    p.space_before = Pt(4)
    add_run_to_p(p, "• Reimbursement Margin Compression: ", bold=True, size=Pt(10), color=NAVY)
    add_run_to_p(p, "Increasing shares of Medicare and Medicaid capped-rate patients limit revenue recovery, pushing median acute hospital operating margins to a razor-thin +0.93%.\n", size=Pt(9.5), color=TEXT_DARK)

    p = tf_tl.add_paragraph()
    p.space_before = Pt(4)
    add_run_to_p(p, "• Fixed Capital Underutilization: ", bold=True, size=Pt(10), color=NAVY)
    add_run_to_p(p, "Maintaining empty physical beds incurs continuous maintenance and overhead costs, directly eroding financial resilience during admission downturns [15].", size=Pt(9.5), color=TEXT_DARK)

    # Bottom-Left: The Uniform Metric Fallacy
    _, tf_bl = add_card_panel(s2, Inches(0.75), Inches(4.20), Inches(5.75), Inches(2.80), 
                              "2. The Flaw of Uniform Regulatory Averages", ALERT_RED)
    p = tf_bl.paragraphs[0]
    add_run_to_p(p, "• The 'One-Size-Fits-All' Administrative Trap: ", bold=True, size=Pt(10), color=ALERT_RED)
    add_run_to_p(p, "State regulatory agencies routinely assess hospital operational performance using statewide aggregate averages, penalizing institutions with inherently distinct care missions [4].\n", size=Pt(9.5), color=TEXT_DARK)

    p = tf_bl.add_paragraph()
    p.space_before = Pt(4)
    add_run_to_p(p, "• Extreme Scale & Mission Disparities: ", bold=True, size=Pt(10), color=ALERT_RED)
    add_run_to_p(p, "Comparing a 25-bed rural critical-access facility against an 800-bed state psychiatric institute or a specialized outpatient surgical clinic creates false benchmarks that distort health policy.\n", size=Pt(9.5), color=TEXT_DARK)

    p = tf_bl.add_paragraph()
    p.space_before = Pt(4)
    add_run_to_p(p, "• Necessity for Latent Peer Grouping: ", bold=True, size=Pt(10), color=ALERT_RED)
    add_run_to_p(p, "Objective clustering must precede performance benchmarking so that facilities are evaluated against mathematically genuine operational peers rather than arbitrary statutory categories [1].", size=Pt(9.5), color=TEXT_DARK)

    # Top-Right: Why Machine Learning?
    _, tf_tr = add_card_panel(s2, Inches(6.80), Inches(1.25), Inches(5.75), Inches(2.75), 
                              "3. Why Unsupervised Machine Learning?", TEAL)
    p = tf_tr.paragraphs[0]
    add_run_to_p(p, "• Absence of Pre-Labeled Ground Truth: ", bold=True, size=Pt(10), color=TEAL)
    add_run_to_p(p, "Hospitals cannot be objectively pre-labeled as 'efficient' or 'underperforming' without introducing regulatory bias; unsupervised algorithms discover organic structures directly from empirical data.\n", size=Pt(9.5), color=TEXT_DARK)

    p = tf_tr.add_paragraph()
    p.space_before = Pt(4)
    add_run_to_p(p, "• Simultaneous Multivariate Synthesis: ", bold=True, size=Pt(10), color=TEAL)
    add_run_to_p(p, "Captures complex interactions across 8 dimensions: margins, cost ratios, bed turnover, stay lengths, available capacity readiness, and outpatient visit intensities.\n", size=Pt(9.5), color=TEXT_DARK)

    p = tf_tr.add_paragraph()
    p.space_before = Pt(4)
    add_run_to_p(p, "• Data-Driven Health Administration: ", bold=True, size=Pt(10), color=TEAL)
    add_run_to_p(p, "Enables hospital executives and state health authorities to establish realistic peer-matched operational targets and identify systemic fiscal vulnerabilities [6].", size=Pt(9.5), color=TEXT_DARK)

    # Bottom-Right: Ethical Scope Boundary
    _, tf_br = add_card_panel(s2, Inches(6.80), Inches(4.20), Inches(5.75), Inches(2.80), 
                              "4. Research Scope & Ethical Non-Causal Boundaries", NAVY_LIGHT)
    p = tf_br.paragraphs[0]
    add_run_to_p(p, "• Purely Administrative & Financial Scope: ", bold=True, size=Pt(10), color=NAVY_LIGHT)
    add_run_to_p(p, "This study models operational accounting balance sheets, bed utilization volumes, and staffing ratios reported under California Health and Safety Code standards.\n", size=Pt(9.5), color=TEXT_DARK)

    p = tf_br.add_paragraph()
    p.space_before = Pt(4)
    add_run_to_p(p, "• Strict Non-Causal Research Stance: ", bold=True, size=Pt(10), color=NAVY_LIGHT)
    add_run_to_p(p, "Clustering identifies geometric proximity in multi-dimensional feature space; it does NOT establish causal mechanisms, evaluate clinician medical quality, or predict patient mortality outcomes.\n", size=Pt(9.5), color=TEXT_DARK)

    p = tf_br.add_paragraph()
    p.space_before = Pt(4)
    add_run_to_p(p, "• Academic Integrity Verification: ", bold=True, size=Pt(10), color=NAVY_LIGHT)
    add_run_to_p(p, "Conducted with full reproducibility: public datasets, fixed seeds, open-source scientific Python stack, zero proprietary dependencies, and strict plagiarism compliance.", size=Pt(9.5), color=TEXT_DARK)

    # =========================================================================
    # SLIDE 3: PROJECT OBJECTIVES & SCOPE (4 Rich Cards + Bottom Summary Banner)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s3)
    create_header(s3, "Project Objectives & Scope of Work", "RESEARCH OBJECTIVES", 3)

    objs = [
        ("1. Multi-Quarter Regulatory Ingestion & Hygiene", Inches(0.75), Inches(1.25), Inches(5.75), Inches(2.55), TEAL, [
            ("California HCAI Data Pipeline: ", "Ingest 5 consecutive quarters (2,192 records) from HealthData.gov."),
            ("Rigorous Entity Filtering: ", "Prune 3 permanently closed facilities and 6 zero-bed/discharge anomalies."),
            ("Annualized Calendar Normalization: ", "Aggregate 4 quarters of 2023 for 428 continuously reporting hospitals."),
            ("Zero Missingness Audit: ", "Achieve 0.0% missing data across all engineered indicators prior to scaling.")
        ]),
        ("2. Clinical-Financial Feature Engineering", Inches(6.80), Inches(1.25), Inches(5.75), Inches(2.55), NAVY, [
            ("8 Multi-Dimensional Indicators: ", "Formulate operating margins, cost ratios, revenue/bed, occupancy, ALOS."),
            ("Administrative Matrix Decoupling: ", "Exclude statutory IDs (FAC_NO, Control Type, County) from feature space."),
            ("Mathematical Division Safety: ", "Implement epsilon-guarded denominators in all ratio formulations."),
            ("Robust Scaling & Winsorization: ", "Apply 1st–99th percentile truncation and RobustScaler (median and IQR).")
        ]),
        ("3. Tri-Algorithm Comparative Evaluation (64 Runs)", Inches(0.75), Inches(3.95), Inches(5.75), Inches(2.35), NAVY, [
            ("Partitioning Benchmark: ", "K-Means (k=2..10) with k-means++ seeding, 10 restarts, fixed random_state=42."),
            ("Hierarchical Exploration: ", "Agglomerative clustering with Ward, Average, and Complete linkage across k=2..10."),
            ("Density & Anomaly Modeling: ", "DBSCAN sweep across 28 grid combinations of eps [0.8..2.5] and MinPts [3..10]."),
            ("Mathematical Validation: ", "Evaluate Silhouette Coefficient, Davies–Bouldin Index, and Calinski–Harabasz Index.")
        ]),
        ("4. Archetype Synthesis & Decision Dashboard", Inches(6.80), Inches(3.95), Inches(5.75), Inches(2.35), TEAL, [
            ("Quantitative Archetype Profiles: ", "Compute centroid medians and clinical operational interpretations for k=4 tiers."),
            ("Interactive Streamlit Application: ", "Deploy multi-module web dashboard with live filtering, PCA, and CSV export."),
            ("Academic Research Deliverables: ", "6-page IEEE conference paper + verified literature review (15 papers, 2021-2026)."),
            ("Reproducible Open-Source Repository: ", "Commit full codebase, notebooks, and benchmarks to GitHub.")
        ])
    ]

    for title, left, top, w, h, col, bullets in objs:
        _, tf_o = add_card_panel(s3, left, top, w, h, title, col)
        for i, (b_lead, b_desc) in enumerate(bullets):
            p = tf_o.paragraphs[0] if i == 0 else tf_o.add_paragraph()
            if i > 0:
                p.space_before = Pt(4)
            add_run_to_p(p, "• " + b_lead, bold=True, size=Pt(9.5), color=col)
            add_run_to_p(p, b_desc, size=Pt(9), color=TEXT_DARK)

    # Bottom Full-Width Scope Banner (Y=6.45 to 7.00, height 0.55")
    s3_b = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(6.45), Inches(11.80), Inches(0.55))
    s3_b.fill.solid()
    s3_b.fill.fore_color.rgb = TEAL_LIGHT
    s3_b.line.color.rgb = TEAL
    s3_b.line.width = Pt(1.0)
    tb_s3b = s3.shapes.add_textbox(Inches(0.9), Inches(6.48), Inches(11.5), Inches(0.48))
    tf_s3b = tb_s3b.text_frame
    tf_s3b.word_wrap = True
    p_s3b = tf_s3b.paragraphs[0]
    add_run_to_p(p_s3b, "Key Academic Deliverables: ", bold=True, size=Pt(10), color=TEAL_DARK)
    add_run_to_p(p_s3b, "Full IEEE Conference Paper (6 pages)  |  14-Slide Executive Presentation  |  Interactive Streamlit App (localhost:8501)  |  Reproducible GitHub Repository (Aditya09977/healthcare)", size=Pt(9.5), color=TEXT_DARK)

    # =========================================================================
    # SLIDE 4: RELATED LITERATURE REVIEW (15 Papers across 3 Columns + Bottom Gap)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s4)
    create_header(s4, "Related Literature Review (15 Verified Papers, 2021-2026)", "LITERATURE REVIEW", 4)

    lit_cols = [
        ("I. Multi-Stage Efficiency Models", Inches(0.75), NAVY, [
            ("[1] Zarrin et al. (2022)", "Health Care Manag. Sci.", "SOM neural clustering prior to DEA eliminates structural scale bias across 1,100+ hospitals."),
            ("[2] Yousefi et al. (2024)", "Socio-Econ. Plan. Sci.", "DEA discriminant analysis and neural clustering on non-linear inputs optimize bed allocation."),
            ("[3] Hao et al. (2023)", "BMC Health Serv. Res.", "Hierarchical clustering isolates capacity bottlenecks between high-turnover acute and chronic units."),
            ("[8] Joynt Maddox et al. (2022)", "PLOS ONE", "Negative operating margins track fixed bed underutilization rather than low clinical demand (3,000+ facilities)."),
            ("[9] Qin et al. (2025)", "Frontiers Public Health", "Two-stage longitudinal DEA and clustering prove growing post-pandemic efficiency divergence.")
        ]),
        ("II. Facility Typologies & Scale", Inches(4.70), TEAL, [
            ("[4] Benmoussa et al. (2024)", "BMC Health Serv. Res.", "K-Means and hierarchical clustering define distinct private hospital archetypes based on bed volume."),
            ("[5] Desai et al. (2023)", "IEEE Access", "Benchmarked K-Means against deep embedded models; proved classical clustering offers superior explainability."),
            ("[6] Vosoughi et al. (2024)", "PLOS ONE", "PCA and K-Means segment trauma centers along surgical volume, payer-mix, and fiscal vulnerability."),
            ("[10] Vluggen et al. (2023)", "BMC Health Serv. Res.", "Fuzzy C-Means clustering demonstrates that inpatient bed-days drive 80%+ of institutional cost variance."),
            ("[16] Khuntia et al. (2022)", "J. Med. Internet Res.", "Ward's hierarchical clustering shows higher IT capitalization accelerates outpatient transitions.")
        ]),
        ("III. Resource Dynamics & Density", Inches(8.65), NAVY_LIGHT, [
            ("[11] Jousilahti et al. (2023)", "BMC Health Serv. Res.", "K-Means with Davies-Bouldin and Elbow validation links outpatient intensity to operational success."),
            ("[12] Al-Makhadmeh et al. (2023)", "Healthcare (MDPI)", "DBSCAN effectively identifies outlier healthcare records without imposing spherical assumptions."),
            ("[13] Jiang et al. (2024)", "Comput. Biol. Med.", "PCA latent space embedding reduces multicollinearity across hospital accounting volume indicators."),
            ("[14] Piccialli et al. (2021)", "Scientific Reports", "Unsupervised outpatient-to-inpatient ratio clustering predicts hospital capacity bottlenecks."),
            ("[15] Schreyögg et al. (2023)", "Health Economics", "Optimal cost efficiency achieved at 75-85% bed occupancy; underutilized beds induce margin collapse.")
        ])
    ]

    for title, left, col, papers in lit_cols:
        _, tf_c = add_card_panel(s4, left, Inches(1.25), Inches(3.90), Inches(4.30), title, col)
        for i, (p_auth, p_ven, p_find) in enumerate(papers):
            p = tf_c.paragraphs[0] if i == 0 else tf_c.add_paragraph()
            if i > 0:
                p.space_before = Pt(4)
            add_run_to_p(p, p_auth + " ", bold=True, size=Pt(9), color=col)
            add_run_to_p(p, f"[{p_ven}]: ", italic=True, size=Pt(8.5), color=TEXT_MUTED)
            add_run_to_p(p, p_find, size=Pt(8.5), color=TEXT_DARK)

    # Bottom Full-Width Research Gap Card (Y=5.65 to 7.00, height 1.35")
    _, tf_gap = add_card_panel(s4, Inches(0.75), Inches(5.65), Inches(11.80), Inches(1.35), 
                               "Identified Research Gap & Novel CA3 Project Contribution", ALERT_RED)
    p_g = tf_gap.paragraphs[0]
    add_run_to_p(p_g, "Prior Literature Gap: ", bold=True, size=Pt(10), color=ALERT_RED)
    add_run_to_p(p_g, "Previous healthcare analytics literature predominantly focused on either patient clinical micro-cohorts or macroscopic spatial logistics, rarely uniting audited statutory accounting balance sheets with physical bed capacity readiness under an objective multi-algorithm machine learning framework [1], [5].\n", size=Pt(9.5), color=TEXT_DARK)
    
    p_g2 = tf_gap.add_paragraph()
    p_g2.space_before = Pt(3)
    add_run_to_p(p_g2, "Our Contribution: ", bold=True, size=Pt(10), color=TEAL_DARK)
    add_run_to_p(p_g2, "We bridge this gap by harmonizing 5 consecutive quarters of California state regulatory filings into annualized profiles, engineering 8 clinical-financial indicators, and executing a systematic 64-run comparative benchmark across K-Means, Agglomerative Hierarchical, and DBSCAN algorithms.", size=Pt(9.5), color=TEXT_DARK)

    # =========================================================================
    # SLIDE 5: DATASET INSPECTION & FEATURE DICTIONARY (Left KPIs + Right Table)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s5)
    create_header(s5, "Dataset Inspection & Feature Engineering Dictionary", "DATASET & FEATURES", 5)

    # Left Column: Ingestion KPIs & Hygiene (Width 4.5", Y=1.25 to 7.00)
    _, tf_ds1 = add_card_panel(s5, Inches(0.75), Inches(1.25), Inches(4.50), Inches(2.75), 
                               "Dataset Provenance & Cohort Audit", NAVY)
    ds_stats = [
        ("Source Authority", "California HCAI / HealthData.gov (ID: 8j3z-qxvr)"),
        ("Filings Audited", "5 Quarters: 2023 Q1–Q4 & 2024 Q1 (2,192 records)"),
        ("Analytical Cohort", "428 Hospitals (Annualized Calendar Year 2023)"),
        ("Pruned Exclusions", "3 Closed facilities excluded; 6 inactive records pruned"),
        ("Feature Missingness", "0.0% across all 8 indicators (zero imputation needed)"),
        ("Reporting Framework", "California Uniform Hospital Accounting & Reporting")
    ]
    for i, (k, v) in enumerate(ds_stats):
        p = tf_ds1.paragraphs[0] if i == 0 else tf_ds1.add_paragraph()
        if i > 0:
            p.space_before = Pt(3)
        add_run_to_p(p, k + ": ", bold=True, size=Pt(9), color=TEAL)
        add_run_to_p(p, v, size=Pt(8.5), color=TEXT_DARK)

    _, tf_ds2 = add_card_panel(s5, Inches(0.75), Inches(4.15), Inches(4.50), Inches(2.85), 
                               "Data Hygiene & Annual Normalization", TEAL)
    hyg_bullets = [
        ("Calendar Year Aggregation: ", "Aggregated 4 quarters of 2023 disclosures to neutralize intra-year seasonal spikes in respiratory admissions and vacation staffing shortages."),
        ("Zero-Division Protection: ", "Incorporated epsilon guards (eps=1e-6) into all bed and discharge denominators to prevent computational runtime exceptions."),
        ("Extreme Ratio Winsorization: ", "Truncated extreme values at 1st and 99th percentiles to stop single-facility reporting errors from distorting Euclidean distance matrices."),
        ("Matrix Decoupling: ", "Statutory identifiers (FAC_NO, County, Control Type) are strictly preserved for downstream drilldown but decoupled from clustering feature matrix X.")
    ]
    for i, (k, v) in enumerate(hyg_bullets):
        p = tf_ds2.paragraphs[0] if i == 0 else tf_ds2.add_paragraph()
        if i > 0:
            p.space_before = Pt(4)
        add_run_to_p(p, "• " + k, bold=True, size=Pt(9.5), color=NAVY)
        add_run_to_p(p, v, size=Pt(8.5), color=TEXT_DARK)

    # Right Column: Engineered Features Table (Width 7.10", Y=1.25 to 7.00, height 5.75")
    t_shape = s5.shapes.add_table(9, 4, Inches(5.45), Inches(1.25), Inches(7.10), Inches(5.75))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(1.50)
    tbl.columns[1].width = Inches(1.65)
    tbl.columns[2].width = Inches(2.95)
    tbl.columns[3].width = Inches(1.00)

    headers = [("INDICATOR", PP_ALIGN.LEFT), ("NAME", PP_ALIGN.LEFT), 
               ("MATHEMATICAL FORMULATION", PP_ALIGN.LEFT), ("SCALE / UNIT", PP_ALIGN.CENTER)]
    for col_idx, (h_text, align) in enumerate(headers):
        style_cell(tbl.cell(0, col_idx), h_text, bold=True, size=Pt(9.5), color=WHITE, bg_color=NAVY, align=align)

    feats_data = [
        ("OP_MARGIN", "Operating Margin", "(Net Revenue - Operating Expense) / Net Revenue", "Ratio"),
        ("EXP_REV_RATIO", "Expense/Rev Ratio", "Total Operating Expense / Total Net Revenue", "Ratio"),
        ("REV_PER_BED", "Revenue per Bed", "Annual Net Operating Revenue / Available Beds", "$ / Bed"),
        ("EXP_PER_BED", "Expense per Bed", "Annual Operating Expense / Available Beds", "$ / Bed"),
        ("OCCUPANCY_RATE", "Bed Occupancy", "Inpatient Days / (Available Beds × 365.25)", "Percentage"),
        ("STF_AVL_RATIO", "Staffed Bed Ratio", "Staffed Beds / Available Beds (Capacity Readiness)", "Ratio"),
        ("ALOS", "Length of Stay", "Total Inpatient Bed Days / Total Patient Discharges", "Days"),
        ("OUTPATIENT_RATIO", "Outpatient Intensity", "Total Outpatient Visits / Total Inpatient Bed Days", "Ratio")
    ]
    for row_idx, (code, name, form, unit) in enumerate(feats_data, start=1):
        bg = ROW_ALT if row_idx % 2 == 1 else WHITE
        style_cell(tbl.cell(row_idx, 0), code, bold=True, size=Pt(9), color=NAVY, bg_color=bg)
        style_cell(tbl.cell(row_idx, 1), name, bold=False, size=Pt(9), color=TEAL_DARK, bg_color=bg)
        style_cell(tbl.cell(row_idx, 2), form, bold=False, size=Pt(8.5), color=TEXT_DARK, bg_color=bg)
        style_cell(tbl.cell(row_idx, 3), unit, bold=True, size=Pt(8.5), color=NAVY, bg_color=bg, align=PP_ALIGN.CENTER)

    # =========================================================================
    # SLIDE 6: END-TO-END SYSTEM ARCHITECTURE (Image Centered + 3 Pillars)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s6)
    create_header(s6, "End-to-End System Architecture", "SYSTEM ARCHITECTURE", 6)

    arch_img = os.path.join("figures", "architecture_diagram.png")
    if os.path.exists(arch_img):
        s6.shapes.add_picture(arch_img, Inches(0.75), Inches(1.25), Inches(11.80), Inches(4.00))

    # Bottom 3 Architecture Pillars (Y=5.35 to 7.00, height 1.65")
    arch_cards = [
        ("Pillar 1: Data Ingestion & Hygiene", Inches(0.75), TEAL, [
            ("Automated Extraction: ", "Parses multi-quarter California HCAI regulatory disclosures."),
            ("Sanitization: ", "Prunes non-operating records; applies epsilon safe-division."),
            ("Winsorization: ", "1st-99th percentile truncation eliminates fat-tail outliers.")
        ]),
        ("Pillar 2: Tri-Algorithm Benchmarking", Inches(4.70), NAVY, [
            ("Model Execution: ", "Runs K-Means, Agglomerative Hierarchical, and DBSCAN in parallel."),
            ("Parameter Grid: ", "Sweeps 64 combinations of k, linkages, eps, and MinPts."),
            ("Metric Triangulation: ", "Evaluates Silhouette, Davies-Bouldin, and Calinski-Harabasz.")
        ]),
        ("Pillar 3: Analytics Delivery & Web App", Inches(8.65), NAVY_LIGHT, [
            ("Streamlit UI: ", "Interactive 6-module dashboard running locally on port 8501."),
            ("PCA Visualizer: ", "Dynamic 2D scatter plot with cluster inspection and search."),
            ("Open Source: ", "Code, notebooks, report, and slide deck pushed to GitHub.")
        ])
    ]
    for title, left, col, items in arch_cards:
        _, tf_a = add_card_panel(s6, left, Inches(5.35), Inches(3.90), Inches(1.65), title, col)
        for i, (k, v) in enumerate(items):
            p = tf_a.paragraphs[0] if i == 0 else tf_a.add_paragraph()
            if i > 0:
                p.space_before = Pt(3)
            add_run_to_p(p, "• " + k, bold=True, size=Pt(9), color=col)
            add_run_to_p(p, v, size=Pt(8.5), color=TEXT_DARK)

    # =========================================================================
    # SLIDE 7: DATA PREPROCESSING & ROBUST SCALING PIPELINE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s7)
    create_header(s7, "Data Preprocessing & Robust Scaling Pipeline", "PREPROCESSING PIPELINE", 7)

    prep_img = os.path.join("figures", "preprocessing_workflow.png")
    if os.path.exists(prep_img):
        s7.shapes.add_picture(prep_img, Inches(0.75), Inches(1.25), Inches(5.80), Inches(4.00))

    # Under-Image Summary Card (Y=5.35 to 7.00, height 1.65")
    _, tf_u = add_card_panel(s7, Inches(0.75), Inches(5.35), Inches(5.80), Inches(1.65), 
                             "Ingestion & Transformation Audit Summary", TEAL)
    p_u1 = tf_u.paragraphs[0]
    add_run_to_p(p_u1, "• 2,192 Raw Hospital-Quarters -> 428 Annual Facilities: ", bold=True, size=Pt(9.5), color=TEAL_DARK)
    add_run_to_p(p_u1, "Consolidates all four 2023 quarters into calendar-year totals (365.25 days), eliminating intra-year seasonality.\n", size=Pt(9), color=TEXT_DARK)
    p_u2 = tf_u.add_paragraph()
    p_u2.space_before = Pt(3)
    add_run_to_p(p_u2, "• Complete Indicator Integrity: ", bold=True, size=Pt(9.5), color=TEAL_DARK)
    add_run_to_p(p_u2, "Zero missingness across all 8 indicators (0.0%). Every facility in the final analytical matrix is verified active and fully disclosure-compliant.", size=Pt(9), color=TEXT_DARK)

    # Right Column: Two Stacked Cards (Y=1.25 to 4.10, Y=4.25 to 7.00)
    _, tf_r1 = add_card_panel(s7, Inches(6.75), Inches(1.25), Inches(5.80), Inches(2.85), 
                              "Mathematical Hygiene & Ratio Safety", NAVY)
    r1_points = [
        ("Record Exclusions: ", "3 closed facilities and 6 inactive entries with zero available beds or discharges were pruned to eliminate non-operational noise."),
        ("Safe Division Formulation: ", "All 8 ratio calculations employ epsilon-guarded denominators (val / (beds + 1e-6)) to guarantee zero division-by-zero crashes."),
        ("1st–99th Percentile Winsorization: ", "Financial metrics exhibit heavy tails. Extreme ratios are clipped to empirical 1st and 99th percentiles:"),
        ("Formula: ", "x_clipped = min( max(x, Q_0.01), Q_0.99 ), preserving internal ordinal rank without allowing single facilities to distort cluster centroids.")
    ]
    for i, (k, v) in enumerate(r1_points):
        p = tf_r1.paragraphs[0] if i == 0 else tf_r1.add_paragraph()
        if i > 0:
            p.space_before = Pt(4)
        add_run_to_p(p, "• " + k, bold=True, size=Pt(9.5), color=NAVY)
        add_run_to_p(p, v, size=Pt(9), color=TEXT_DARK)

    _, tf_r2 = add_card_panel(s7, Inches(6.75), Inches(4.25), Inches(5.80), Inches(2.75), 
                              "Why RobustScaler over StandardScaler?", TEAL_DARK)
    r2_points = [
        ("The Limitation of StandardScaler: ", "StandardScaler centers on the sample mean and divides by standard deviation. Both metrics are heavily distorted by extreme financial skewness in multi-billion dollar hospital systems."),
        ("RobustScaler Formulation: ", "Centers using the median and scales by the Interquartile Range (IQR):"),
        ("Mathematical Equation: ", "x' = (x - Q2) / (Q3 - Q1), where Q2 is the median and IQR = Q3 - Q1."),
        ("Analytical Advantage: ", "Normalizes the middle 50% of healthcare facilities to a standard scale while robustly handling valid long-stay and specialty surgical outliers.")
    ]
    for i, (k, v) in enumerate(r2_points):
        p = tf_r2.paragraphs[0] if i == 0 else tf_r2.add_paragraph()
        if i > 0:
            p.space_before = Pt(4)
        add_run_to_p(p, "• " + k, bold=True, size=Pt(9.5), color=TEAL_DARK)
        add_run_to_p(p, v, size=Pt(9), color=TEXT_DARK)

    # =========================================================================
    # SLIDE 8: THREE CLUSTERING PARADIGMS (3 Dense Pillars + Bottom Summary)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s8)
    create_header(s8, "Three Primary Clustering Paradigms", "CLUSTERING METHODOLOGY", 8)

    pillars = [
        ("A. K-Means (Partitioning)", Inches(0.75), TEAL, [
            ("Mathematical Core: ", "Minimizes within-cluster sum of squared Euclidean errors (inertia) around k centroids."),
            ("Tested Hyperparameters: ", "k in {2..10}, k-means++ seeding, 10 restarts, max_iter=300, seed=42 (9 runs)."),
            ("Time Complexity: ", "O(n · k · d · i) — Linear scalability and high computational efficiency (< 0.04s runtime)."),
            ("Distance Metric: ", "Strictly Euclidean distance; assumes spherical, equally dispersed cluster boundaries."),
            ("Key Strengths: ", "Produces explicit, directly interpretable centroids for administrative benchmarking."),
            ("Empirical Selection: ", "Selected k=4 (Silhouette=0.6113, CH=655.84) as the most actionable clinical partition.")
        ]),
        ("B. Agglomerative (Hierarchical)", Inches(4.70), NAVY, [
            ("Mathematical Core: ", "Bottom-up hierarchical tree merge based on pairwise cluster proximity matrix."),
            ("Tested Linkages: ", "Ward (minimum variance), Average (mean distance), Complete (max distance) for k in {2..10} (27 runs)."),
            ("Time & Space Complexity: ", "O(n^2) distance matrix computation; deterministic execution without random seeds."),
            ("Metric Requirements: ", "Ward requires Euclidean distances; Average and Complete accept non-Euclidean metrics."),
            ("Key Strengths: ", "Generates intuitive dendrogram hierarchies; independently validates K-Means structure."),
            ("Empirical Confirmation: ", "Ward linkage at k=4 achieves Silhouette=0.6708, confirming K-Means centroid boundaries.")
        ]),
        ("C. DBSCAN (Density-Based)", Inches(8.65), GOLD, [
            ("Mathematical Core: ", "Discovers dense connected core components; flags sparse non-reachable points as noise (-1)."),
            ("Tested Parameter Grid: ", "eps in {0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5}, MinPts in {3, 5, 8, 10} (28 total runs)."),
            ("Computational Scaling: ", "O(n log n) with spatial indexing; does not require pre-specifying cluster count k."),
            ("Geometric Flexibility: ", "Discovers arbitrary non-convex geometries; immune to spherical assumptions."),
            ("Sensitivity: ", "Struggles with variable density across high-dimensional hospital operational features."),
            ("Empirical Role: ", "Functions as an automated anomaly detector, isolating 4.7% to 10.5% extreme facility outliers.")
        ])
    ]
    for title, left, col, bullets in pillars:
        _, tf_p = add_card_panel(s8, left, Inches(1.25), Inches(3.90), Inches(4.30), title, col)
        for i, (k, v) in enumerate(bullets):
            p = tf_p.paragraphs[0] if i == 0 else tf_p.add_paragraph()
            if i > 0:
                p.space_before = Pt(3.5)
            add_run_to_p(p, "• " + k, bold=True, size=Pt(9), color=col)
            add_run_to_p(p, v, size=Pt(8.5), color=TEXT_DARK)

    # Bottom Tri-Algorithm Rationale Card (Y=5.65 to 7.00, height 1.35")
    _, tf_br = add_card_panel(s8, Inches(0.75), Inches(5.65), Inches(11.80), Inches(1.35), 
                              "Tri-Algorithm Methodological Synthesis & Cross-Paradigm Validation", NAVY)
    p_b1 = tf_br.paragraphs[0]
    add_run_to_p(p_b1, "Triangulation Rationale: ", bold=True, size=Pt(10), color=NAVY)
    add_run_to_p(p_b1, "Evaluating partitioning (K-Means), hierarchical (Agglomerative), and density (DBSCAN) models enables cross-paradigm verification. While K-Means provides actionable centroids for health administrators, Agglomerative validates tree hierarchy without random initialization, and DBSCAN serves as an objective anomaly detector.\n", size=Pt(9.5), color=TEXT_DARK)
    p_b2 = tf_br.add_paragraph()
    p_b2.space_before = Pt(3)
    add_run_to_p(p_b2, "Resulting Consensus: ", bold=True, size=Pt(10), color=TEAL_DARK)
    add_run_to_p(p_b2, "All three paradigms independently confirm that California hospitals divide into a massive general acute core (>90%) surrounded by distinct specialty surgical centers, long-term psychiatric units, and subacute rehab facilities.", size=Pt(9.5), color=TEXT_DARK)

    # =========================================================================
    # SLIDE 9: MATHEMATICAL FORMULATION & METRICS (Dense 2x2 Grid with Callouts)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s9)
    create_header(s9, "Mathematical Formulation & Evaluation Criteria", "MATHEMATICAL EQUATIONS", 9)

    eqs = [
        ("1. K-Means Objective Function (Inertia)", Inches(0.75), Inches(1.25), Inches(5.75), Inches(2.75), TEAL, [
            ("Objective Formulation: ", "Minimizes within-cluster sum of squared Euclidean deviations (intra-cluster scatter):"),
            ("Mathematical Formula: ", "J = sum_{k=1}^K sum_{x_i in S_k} || x_i - mu_k ||^2"),
            ("Notation: ", "x_i is the 8D robust-scaled hospital vector, mu_k is the centroid of cluster S_k."),
            ("Optimization Behavior: ", "Alternates between Voronoi partition assignment and centroid recalculation."),
            ("Empirical Convergence: ", "Inertia drops from 7,865.9 (k=2) to 4,505.5 (k=4); elbow curvature peaks at k=4.")
        ]),
        ("2. Silhouette Coefficient s(i)", Inches(6.80), Inches(1.25), Inches(5.75), Inches(2.75), NAVY, [
            ("Cohesion vs Separation: ", "Quantifies how well a hospital belongs to its assigned cluster vs nearest neighbor:"),
            ("Mathematical Formula: ", "s(i) = [ b(i) - a(i) ] / max( a(i), b(i) ),  where s(i) in [-1, +1]"),
            ("Notation: ", "a(i) = mean distance within same cluster; b(i) = min mean distance to any other cluster."),
            ("Benchmark Scale: ", "s > 0.70 (Strong structure); 0.50 - 0.70 (Reasonable structure); < 0.25 (No structure)."),
            ("Our Model Benchmark: ", "Selected K-Means k=4 achieves s = 0.6113, confirming robust separation without overlap.")
        ]),
        ("3. Davies–Bouldin Index (DB)", Inches(0.75), Inches(4.20), Inches(5.75), Inches(2.80), NAVY, [
            ("Dispersion Ratio: ", "Evaluates worst-case similarity between each cluster and its most proximate competitor:"),
            ("Mathematical Formula: ", "DB = (1/k) sum_{i=1}^k max_{j != i} [ (s_i + s_j) / d(mu_i, mu_j) ]"),
            ("Notation: ", "s_i = average Euclidean distance to centroid mu_i; d(mu_i, mu_j) = distance between centroids."),
            ("Optimization Direction: ", "Lower values indicate superior partitions (tighter clusters, further apart)."),
            ("Our Model Benchmark: ", "Selected K-Means k=4 achieves DB = 0.5768 (well below 0.60 threshold), proving compact cores.")
        ]),
        ("4. Calinski–Harabasz Index (CH)", Inches(6.80), Inches(4.20), Inches(5.75), Inches(2.80), TEAL, [
            ("Variance Ratio Criterion: ", "Ratio of between-cluster dispersion to within-cluster dispersion:"),
            ("Mathematical Formula: ", "CH = [ Tr(B_k) / Tr(W_k) ] * [ (n - k) / (k - 1) ]"),
            ("Notation: ", "B_k = between-group scatter matrix; W_k = within-group scatter matrix; n=428, k=clusters."),
            ("Optimization Direction: ", "Higher values indicate distinct, well-separated clusters with minimal shared variance."),
            ("Our Model Benchmark: ", "Selected K-Means k=4 reaches CH = 655.84, confirming between-cluster separation dominates.")
        ])
    ]
    for title, left, top, w, h, col, items in eqs:
        _, tf_e = add_card_panel(s9, left, top, w, h, title, col)
        for i, (k, v) in enumerate(items):
            p = tf_e.paragraphs[0] if i == 0 else tf_e.add_paragraph()
            if i > 0:
                p.space_before = Pt(3)
            is_formula = "Formula:" in k
            add_run_to_p(p, "• " + k, bold=True, size=Pt(9.5 if is_formula else 9), color=TEAL_DARK if is_formula else col)
            add_run_to_p(p, v, bold=is_formula, size=Pt(9.5 if is_formula else 8.5), color=NAVY if is_formula else TEXT_DARK)

    # =========================================================================
    # SLIDE 10: EXPERIMENTAL ENVIRONMENT & PARAMETER SEARCH GRID (Left Stack + Right Table)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s10)
    create_header(s10, "Experimental Environment & Parameter Search Grid", "EXPERIMENTAL SETUP", 10)

    # Left Column: Software Stack & Reproducibility (Width 4.5", Y=1.25 to 7.00)
    _, tf_env1 = add_card_panel(s10, Inches(0.75), Inches(1.25), Inches(4.50), Inches(2.75), 
                                "Hardware & Software Stack Specifications", NAVY)
    env_specs = [
        ("Host Platform", "Windows 11 OS / x86_64 Architecture"),
        ("Python Version", "Python 3.11.9 (64-bit CPython runtime)"),
        ("Core ML Suite", "Scikit-Learn 1.8.0 (KMeans, Agglomerative, DBSCAN)"),
        ("Data Manipulation", "Pandas 3.0.1, NumPy 2.4.2 (vectorized C arrays)"),
        ("Scientific Computing", "SciPy 1.17.0 (hierarchical linkages & dendrograms)"),
        ("Data Visualization", "Matplotlib 3.11.2, Seaborn 0.13.2"),
        ("Interactive Web App", "Streamlit 1.66.1 (live reactive local server)"),
        ("Execution Overhead", "< 50 MB RAM footprint  |  < 4.0s total runtime")
    ]
    for i, (k, v) in enumerate(env_specs):
        p = tf_env1.paragraphs[0] if i == 0 else tf_env1.add_paragraph()
        if i > 0:
            p.space_before = Pt(2.5)
        add_run_to_p(p, k + ": ", bold=True, size=Pt(9), color=TEAL)
        add_run_to_p(p, v, size=Pt(8.5), color=TEXT_DARK)

    _, tf_env2 = add_card_panel(s10, Inches(0.75), Inches(4.15), Inches(4.50), Inches(2.85), 
                                "Reproducibility & Execution Controls", TEAL)
    rep_bullets = [
        ("Deterministic Random State: ", "Fixed random_state=42 across all stochastic algorithms (K-Means, PCA) guarantees identical reproducibility on any host machine."),
        ("Initialization Protocol: ", "Employed k-means++ probabilistic seeding with 10 random restarts (n_init=10) and 300 maximum iterations to prevent local minima traps."),
        ("Systematic Benchmark Logging: ", "All 64 experimental iterations recorded to results/experiment_results.csv with runtime, noise percentage, and cluster size breakdowns."),
        ("Git Version Control: ", "Codebase version-tracked and pushed to GitHub (Aditya09977/healthcare).")
    ]
    for i, (k, v) in enumerate(rep_bullets):
        p = tf_env2.paragraphs[0] if i == 0 else tf_env2.add_paragraph()
        if i > 0:
            p.space_before = Pt(4)
        add_run_to_p(p, "• " + k, bold=True, size=Pt(9.5), color=NAVY)
        add_run_to_p(p, v, size=Pt(8.5), color=TEXT_DARK)

    # Right Column: Hyperparameter Search Grid Table (Width 7.10", Y=1.25 to 7.00)
    t_shape10 = s10.shapes.add_table(4, 5, Inches(5.45), Inches(1.25), Inches(7.10), Inches(3.20))
    tbl10 = t_shape10.table
    tbl10.columns[0].width = Inches(1.60)
    tbl10.columns[1].width = Inches(1.80)
    tbl10.columns[2].width = Inches(1.50)
    tbl10.columns[3].width = Inches(1.00)
    tbl10.columns[4].width = Inches(1.20)

    h10 = [("ALGORITHM", PP_ALIGN.LEFT), ("SEARCH SPACE", PP_ALIGN.LEFT), 
           ("FIXED HYPERPARAMS", PP_ALIGN.LEFT), ("RUNS", PP_ALIGN.CENTER), ("RUNTIME", PP_ALIGN.CENTER)]
    for c_idx, (h_text, align) in enumerate(h10):
        style_cell(tbl10.cell(0, c_idx), h_text, bold=True, size=Pt(9), color=WHITE, bg_color=NAVY, align=align)

    grid_data = [
        ("K-Means", "k in {2, 3, 4, 5, 6, 7, 8, 9, 10}", "k-means++, n_init=10, seed=42", "9 Runs", "0.034s (avg)"),
        ("Agglomerative", "Linkage: Ward, Avg, Complete\nk in {2, 3, ..., 10}", "Metric: Euclidean\nAffinity: pairwise", "27 Runs", "0.003s (avg)"),
        ("DBSCAN", "eps in {0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5}\nMinPts in {3, 5, 8, 10}", "Metric: Euclidean\nAlgorithm: auto", "28 Runs", "0.002s (avg)")
    ]
    for r_idx, (alg, space, fixed, runs, rt) in enumerate(grid_data, start=1):
        bg = ROW_ALT if r_idx % 2 == 1 else WHITE
        style_cell(tbl10.cell(r_idx, 0), alg, bold=True, size=Pt(9), color=NAVY, bg_color=bg)
        style_cell(tbl10.cell(r_idx, 1), space, bold=False, size=Pt(8.5), color=TEXT_DARK, bg_color=bg)
        style_cell(tbl10.cell(r_idx, 2), fixed, bold=False, size=Pt(8.5), color=TEAL_DARK, bg_color=bg)
        style_cell(tbl10.cell(r_idx, 3), runs, bold=True, size=Pt(9), color=NAVY, bg_color=bg, align=PP_ALIGN.CENTER)
        style_cell(tbl10.cell(r_idx, 4), rt, bold=False, size=Pt(8.5), color=TEXT_DARK, bg_color=bg, align=PP_ALIGN.CENTER)

    # Under-Table Experimental Takeaway Panel (Y=4.65 to 7.00, height 2.35")
    _, tf_t10 = add_card_panel(s10, Inches(5.45), Inches(4.65), Inches(7.10), Inches(2.35), 
                              "Experimental Search Space Synthesis", NAVY_LIGHT)
    p_t1 = tf_t10.paragraphs[0]
    add_run_to_p(p_t1, "• 64 Total Experimental Configurations: ", bold=True, size=Pt(9.5), color=NAVY)
    add_run_to_p(p_t1, "Systematic coverage across partitioning, hierarchical, and density regimes provides complete empirical insight into California healthcare operational topology.\n", size=Pt(9), color=TEXT_DARK)
    p_t2 = tf_t10.add_paragraph()
    p_t2.space_before = Pt(3)
    add_run_to_p(p_t2, "• Computational Efficiency: ", bold=True, size=Pt(9.5), color=NAVY)
    add_run_to_p(p_t2, "All 64 runs executed in under 4 seconds combined on standard commodity hardware, demonstrating that unsupervised machine learning provides immediate operational analytics without massive compute budgets.\n", size=Pt(9), color=TEXT_DARK)
    p_t3 = tf_t10.add_paragraph()
    p_t3.space_before = Pt(3)
    add_run_to_p(p_t3, "• Metric Logging: ", bold=True, size=Pt(9.5), color=NAVY)
    add_run_to_p(p_t3, "Full validation results preserved in results/experiment_results.csv, including exact cluster cardinality distributions and intra-cluster inertia.", size=Pt(9), color=TEXT_DARK)

    # =========================================================================
    # SLIDE 11: COMPARATIVE RESULTS ACROSS MODELS (Left Chart + Right Benchmark Table)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s11)
    create_header(s11, "Comparative Experimental Results Across Models", "BENCHMARK RESULTS", 11)

    elbow_img = os.path.join("figures", "elbow_and_metrics.png")
    if os.path.exists(elbow_img):
        s11.shapes.add_picture(elbow_img, Inches(0.75), Inches(1.25), Inches(5.60), Inches(3.90))

    # Under-Chart Summary Card (Y=5.25 to 7.00, height 1.75")
    _, tf_eb = add_card_panel(s11, Inches(0.75), Inches(5.25), Inches(5.60), Inches(1.75), 
                              "Elbow & Silhouette Curve Analysis", TEAL)
    p_eb1 = tf_eb.paragraphs[0]
    add_run_to_p(p_eb1, "• Inertia Inflection at k=4: ", bold=True, size=Pt(9.5), color=TEAL_DARK)
    add_run_to_p(p_eb1, "Within-cluster inertia drops sharply from k=2 (7,865) to k=4 (4,505), after which marginal gains flatten, indicating diminishing returns for k>4.\n", size=Pt(9), color=TEXT_DARK)
    p_eb2 = tf_eb.add_paragraph()
    p_eb2.space_before = Pt(3)
    add_run_to_p(p_eb2, "• Davies-Bouldin & Calinski-Harabasz: ", bold=True, size=Pt(9.5), color=TEAL_DARK)
    add_run_to_p(p_eb2, "DB remains well below 0.60 (0.5768) and CH reaches 655.84, confirming tight cluster cohesion and strong separation.", size=Pt(9), color=TEXT_DARK)

    # Right Column: Model Comparison Table (Width 6.00", Y=1.25 to 5.15)
    t_shape11 = s11.shapes.add_table(10, 6, Inches(6.55), Inches(1.25), Inches(6.00), Inches(3.85))
    tbl11 = t_shape11.table
    tbl11.columns[0].width = Inches(1.90)
    tbl11.columns[1].width = Inches(0.85)
    tbl11.columns[2].width = Inches(0.80)
    tbl11.columns[3].width = Inches(0.80)
    tbl11.columns[4].width = Inches(0.75)
    tbl11.columns[5].width = Inches(0.90)

    h11 = [("MODEL & CONFIG", PP_ALIGN.LEFT), ("SILHOUETTE", PP_ALIGN.CENTER), 
           ("DB INDEX", PP_ALIGN.CENTER), ("CH INDEX", PP_ALIGN.CENTER), 
           ("NOISE %", PP_ALIGN.CENTER), ("STATUS", PP_ALIGN.CENTER)]
    for c_idx, (h_text, align) in enumerate(h11):
        style_cell(tbl11.cell(0, c_idx), h_text, bold=True, size=Pt(8.5), color=WHITE, bg_color=NAVY, align=align)

    models_data = [
        ("K-Means (k=2)", "0.8818", "0.3102", "950.29", "0.0%", "Unbalanced (97%)"),
        ("K-Means (k=3)", "0.7601", "0.4741", "709.62", "0.0%", "Sub-optimal"),
        ("K-Means (k=4)", "0.6113", "0.5768", "655.84", "0.0%", "SELECTED BEST"),
        ("K-Means (k=5)", "0.5033", "0.8612", "623.68", "0.0%", "Over-split"),
        ("Agglomerative (Ward, k=4)", "0.6708", "0.4634", "638.75", "0.0%", "Strong Benchmark"),
        ("Agglomerative (Avg, k=4)", "0.7005", "0.4660", "524.36", "0.0%", "Valid Benchmark"),
        ("Agglomerative (Comp, k=4)", "0.6925", "0.4996", "574.58", "0.0%", "Valid Benchmark"),
        ("DBSCAN (eps=1.8, min=3)", "0.9352", "0.0615", "1522.79", "10.51%", "Anomaly Detector"),
        ("DBSCAN (eps=2.5, min=3)", "0.6752", "0.3158", "494.45", "4.67%", "Anomaly Detector")
    ]
    for r_idx, (m_name, sil, db, ch, noise, stat) in enumerate(models_data, start=1):
        is_selected = "SELECTED" in stat
        bg = TEAL_LIGHT if is_selected else (ROW_ALT if r_idx % 2 == 1 else WHITE)
        t_col = TEAL_DARK if is_selected else NAVY
        style_cell(tbl11.cell(r_idx, 0), m_name, bold=is_selected, size=Pt(8.5), color=t_col, bg_color=bg)
        style_cell(tbl11.cell(r_idx, 1), sil, bold=is_selected, size=Pt(8.5), color=TEXT_DARK, bg_color=bg, align=PP_ALIGN.CENTER)
        style_cell(tbl11.cell(r_idx, 2), db, bold=is_selected, size=Pt(8.5), color=TEXT_DARK, bg_color=bg, align=PP_ALIGN.CENTER)
        style_cell(tbl11.cell(r_idx, 3), ch, bold=is_selected, size=Pt(8.5), color=TEXT_DARK, bg_color=bg, align=PP_ALIGN.CENTER)
        style_cell(tbl11.cell(r_idx, 4), noise, bold=is_selected, size=Pt(8.5), color=TEXT_DARK, bg_color=bg, align=PP_ALIGN.CENTER)
        style_cell(tbl11.cell(r_idx, 5), stat, bold=True, size=Pt(8), color=SUCCESS_GREEN if is_selected else TEXT_MUTED, bg_color=bg, align=PP_ALIGN.CENTER)

    # Right Under-Table Rationale Card (Y=5.25 to 7.00, height 1.75")
    _, tf_sel = add_card_panel(s11, Inches(6.55), Inches(5.25), Inches(6.00), Inches(1.75), 
                              "Empirical Model Selection Rationale", ALERT_RED)
    p_s1 = tf_sel.paragraphs[0]
    add_run_to_p(p_s1, "Why k=4 over k=2? ", bold=True, size=Pt(9.5), color=ALERT_RED)
    add_run_to_p(p_s1, "While k=2 produces higher mathematical Silhouette (0.8818), it groups 417 out of 428 hospitals (97.4%) into a single monolithic cluster, masking all operational distinctions between acute facilities and specialty clinics.\n", size=Pt(9), color=TEXT_DARK)
    p_s2 = tf_sel.add_paragraph()
    p_s2.space_before = Pt(3)
    add_run_to_p(p_s2, "Actionable Partitioning: ", bold=True, size=Pt(9.5), color=TEAL_DARK)
    add_run_to_p(p_s2, "K-Means at k=4 achieves strong statistical validity (Silhouette=0.6113, DB=0.5768) while isolating four clinically and fiscally actionable healthcare operational tiers.", size=Pt(9), color=TEXT_DARK)

    # =========================================================================
    # SLIDE 12: DISCOVERED HEALTHCARE ARCHETYPES (Top 4 Cards + Bottom PCA & Table)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s12)
    create_header(s12, "Discovered Healthcare Facility Archetypes (k=4 Solution)", "CLUSTER PROFILES", 12)

    # Top 4 Archetype Cards (Y=1.25 to 3.10, height 1.85", spanning width 11.8")
    arch_panels = [
        ("Cluster 0: General Acute", "388 Hospitals (90.7%)", TEAL, [
            ("Avg Beds: 204", "ALOS: 5.7 days"),
            ("Operating Margin: +0.93%", "Break-even"),
            ("Rev/Bed: $1.31M", "Exp/Bed: $1.38M")
        ]),
        ("Cluster 1: State Long-Term", "8 Facilities (1.9%)", ALERT_RED, [
            ("Avg Beds: 795", "ALOS: 403 days"),
            ("Operating Margin: -48.20%", "Subsidized"),
            ("Rev/Bed: $217k", "Occupancy: 92.0%")
        ]),
        ("Cluster 2: Subacute Rehab", "12 Facilities (2.8%)", GOLD, [
            ("Avg Beds: 168", "ALOS: 122 days"),
            ("Operating Margin: -9.46%", "Recovery"),
            ("Rev/Bed: $362k", "Occupancy: 74.4%")
        ]),
        ("Cluster 3: Specialty Surgical", "20 Centers (4.7%)", SUCCESS_GREEN, [
            ("Avg Beds: 40", "ALOS: 3.6 days"),
            ("Operating Margin: +3.12%", "Profitable"),
            ("Rev/Bed: $3.58M", "3x Acute Baseline")
        ])
    ]
    for idx, (title, sub, col, rows) in enumerate(arch_panels):
        left_pos = Inches(0.75 + idx * 2.97)
        _, tf_ap = add_card_panel(s12, left_pos, Inches(1.25), Inches(2.82), Inches(1.85), title, col)
        p_sub = tf_ap.paragraphs[0]
        p_sub.text = sub
        p_sub.font.size = Pt(9.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = col

        for r_left, r_right in rows:
            p_r = tf_ap.add_paragraph()
            p_r.space_before = Pt(2)
            add_run_to_p(p_r, "• " + r_left + "  |  ", bold=True, size=Pt(8.5), color=NAVY)
            add_run_to_p(p_r, r_right, size=Pt(8.5), color=TEXT_DARK)

    # Bottom-Left: PCA Scatter Plot (Y=3.25 to 7.00, height 3.75", width 5.8")
    pca_img = os.path.join("figures", "pca_clusters.png")
    if os.path.exists(pca_img):
        s12.shapes.add_picture(pca_img, Inches(0.75), Inches(3.25), Inches(5.80), Inches(3.75))

    # Bottom-Right: Detailed Archetype Metrics Table & Policy Takeaways (Y=3.25 to 7.00)
    t_shape12 = s12.shapes.add_table(5, 6, Inches(6.75), Inches(3.25), Inches(5.80), Inches(1.95))
    tbl12 = t_shape12.table
    tbl12.columns[0].width = Inches(1.45)
    tbl12.columns[1].width = Inches(0.75)
    tbl12.columns[2].width = Inches(0.90)
    tbl12.columns[3].width = Inches(0.90)
    tbl12.columns[4].width = Inches(0.90)
    tbl12.columns[5].width = Inches(0.90)

    h12 = [("ARCHETYPE", PP_ALIGN.LEFT), ("COUNT", PP_ALIGN.CENTER), 
           ("MARGIN", PP_ALIGN.CENTER), ("OCCUPANCY", PP_ALIGN.CENTER), 
           ("ALOS", PP_ALIGN.CENTER), ("REV / BED", PP_ALIGN.CENTER)]
    for c_idx, (h_text, align) in enumerate(h12):
        style_cell(tbl12.cell(0, c_idx), h_text, bold=True, size=Pt(8.5), color=WHITE, bg_color=NAVY, align=align)

    t12_data = [
        ("C0: General Acute", "388 (90.7%)", "+0.93%", "65.3%", "5.7 days", "$1.31M"),
        ("C1: State Long-Term", "8 (1.9%)", "-48.20%", "92.0%", "403.2 days", "$0.22M"),
        ("C2: Subacute Rehab", "12 (2.8%)", "-9.46%", "74.4%", "122.2 days", "$0.36M"),
        ("C3: Specialty Surgical", "20 (4.7%)", "+3.12%", "33.0%", "3.6 days", "$3.58M")
    ]
    for r_idx, (c_name, cnt, mrg, occ, alos, rpb) in enumerate(t12_data, start=1):
        bg = ROW_ALT if r_idx % 2 == 1 else WHITE
        style_cell(tbl12.cell(r_idx, 0), c_name, bold=True, size=Pt(8.5), color=NAVY, bg_color=bg)
        style_cell(tbl12.cell(r_idx, 1), cnt, bold=False, size=Pt(8.5), color=TEXT_DARK, bg_color=bg, align=PP_ALIGN.CENTER)
        style_cell(tbl12.cell(r_idx, 2), mrg, bold=True, size=Pt(8.5), color=ALERT_RED if "-" in mrg else SUCCESS_GREEN, bg_color=bg, align=PP_ALIGN.CENTER)
        style_cell(tbl12.cell(r_idx, 3), occ, bold=False, size=Pt(8.5), color=TEXT_DARK, bg_color=bg, align=PP_ALIGN.CENTER)
        style_cell(tbl12.cell(r_idx, 4), alos, bold=False, size=Pt(8.5), color=TEXT_DARK, bg_color=bg, align=PP_ALIGN.CENTER)
        style_cell(tbl12.cell(r_idx, 5), rpb, bold=True, size=Pt(8.5), color=TEAL_DARK, bg_color=bg, align=PP_ALIGN.CENTER)

    # Bottom-Right Policy Implications Card (Y=5.35 to 7.00, height 1.65")
    _, tf_pol = add_card_panel(s12, Inches(6.75), Inches(5.35), Inches(5.80), Inches(1.65), 
                              "Operational Insights & Health Policy Takeaways", NAVY)
    p_pol1 = tf_pol.paragraphs[0]
    add_run_to_p(p_pol1, "• Acute Community Vulnerability (90.7%): ", bold=True, size=Pt(9), color=TEAL)
    add_run_to_p(p_pol1, "California's acute care backbone operates on razor-thin +0.93% margins, rendering it vulnerable to minor wage or inflation shocks.\n", size=Pt(8.5), color=TEXT_DARK)
    p_pol2 = tf_pol.add_paragraph()
    p_pol2.space_before = Pt(3)
    add_run_to_p(p_pol2, "• High Capital Velocity in Specialty Centers: ", bold=True, size=Pt(9), color=SUCCESS_GREEN)
    add_run_to_p(p_pol2, "Cluster 3 generates nearly 3x higher revenue per bed ($3.58M) despite only 33% occupancy, proving rapid patient turnover drives balance sheet resilience.", size=Pt(8.5), color=TEXT_DARK)

    # =========================================================================
    # SLIDE 13: INTERACTIVE STREAMLIT DASHBOARD (Left Image + Right Feature Cards)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s13)
    create_header(s13, "Interactive Analytics Dashboard (Streamlit)", "DASHBOARD DEMONSTRATION", 13)

    dash_img = os.path.join("figures", "dashboard_screenshot.png")
    if os.path.exists(dash_img):
        s13.shapes.add_picture(dash_img, Inches(0.75), Inches(1.25), Inches(6.40), Inches(4.00))

    # Under-Screenshot Terminal Callout (Y=5.35 to 7.00, height 1.65")
    _, tf_cmd = add_card_panel(s13, Inches(0.75), Inches(5.35), Inches(6.40), Inches(1.65), 
                               "Live Execution & Operational Verification", TEAL)
    p_c1 = tf_cmd.paragraphs[0]
    add_run_to_p(p_c1, "Live CLI Command: ", bold=True, size=Pt(9.5), color=NAVY)
    add_run_to_p(p_c1, "streamlit run app.py --server.headless true --server.port 8501\n", bold=True, size=Pt(9), color=TEAL_DARK)
    p_c2 = tf_cmd.add_paragraph()
    p_c2.space_before = Pt(3)
    add_run_to_p(p_c2, "Deployment Architecture: ", bold=True, size=Pt(9.5), color=NAVY)
    add_run_to_p(p_c2, "Pure Python and Streamlit implementation running locally on port 8501 with zero cloud latency. Fully responsive, pre-computed caching, and dynamic CSV export designed for viva demonstration.", size=Pt(8.5), color=TEXT_DARK)

    # Right Column: 6 Structured Dashboard Modules (Width 5.15", Y=1.25 to 7.00, height 5.75")
    _, tf_mod = add_card_panel(s13, Inches(7.40), Inches(1.25), Inches(5.15), Inches(5.75), 
                               "Streamlit Analytical Modules (6 Tabs)", NAVY)
    modules = [
        ("Module A: Dataset Overview & Quality Audit", "Interactive audit cards for 2,192 filings, control-type distribution charts, missingness checks, and data hygiene checklists."),
        ("Module B: Financial Performance Explorer", "Interactive histograms of operating margins, expense-to-revenue ratio scatter plots, and break-even vulnerability analysis."),
        ("Module C: Resource Utilization Metrics", "Bed occupancy rate boxplots, average length of stay (ALOS) distributions, and staffed-to-available bed readiness ratios."),
        ("Module D: 2D PCA Cluster Explorer", "Interactive PCA projection with live county and cluster filters, dynamic facility search, and instant filtered CSV download."),
        ("Module E: Tri-Model Benchmark Table", "Complete quantitative comparison table evaluating K-Means, Agglomerative, and DBSCAN across Silhouette, DB, and CH metrics."),
        ("Module F: Insights & Limitations", "Actionable health policy takeaways, clinical non-causality disclaimers, and academic integrity verification checklists.")
    ]
    for i, (m_title, m_desc) in enumerate(modules):
        p = tf_mod.paragraphs[0] if i == 0 else tf_mod.add_paragraph()
        if i > 0:
            p.space_before = Pt(5)
        add_run_to_p(p, "• " + m_title + ":\n", bold=True, size=Pt(9.5), color=TEAL)
        add_run_to_p(p, m_desc, size=Pt(8.5), color=TEXT_DARK)

    # =========================================================================
    # SLIDE 14: CONCLUSION, LIMITATIONS & FUTURE SCOPE (Full 2-Tier Balanced Layout)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s14)
    create_header(s14, "Conclusion, Limitations & Future Scope", "CONCLUSION & OUTLOOK", 14)

    # Top Tier: 3 Columns (Y=1.25 to 5.00, height 3.75", Width 3.75" each)
    tier1_cards = [
        ("I. Core Project Conclusions", Inches(0.75), TEAL, [
            ("End-to-End Execution: ", "Built complete automated ingestion, schema validation, 8-feature engineering, and live dashboard."),
            ("Empirical Model Selection: ", "K-Means at k=4 validated as mathematically robust (Sil=0.6113, DB=0.5768, CH=655.84)."),
            ("Acute Care Vulnerability: ", "90.7% of California hospitals operate on thin +0.93% margins, highly sensitive to labor inflation."),
            ("Specialty Surgical Velocity: ", "Specialty centers generate nearly 3x higher revenue per bed ($3.58M) despite lower occupancy (33.0%)."),
            ("Academic Deliverables: ", "6-page IEEE paper, 15 verified citations, and reproducible GitHub repository.")
        ]),
        ("II. Methodological Limitations", Inches(4.78), ALERT_RED, [
            ("Strict Non-Causal Scope: ", "Unsupervised clustering discovers geometrical associations; it does not prove clinical care quality or patient mortality."),
            ("Public Accounting Heterogeneity: ", "Government facilities report under public fund accounting, creating statutory deficits distinct from private GAAP filings."),
            ("Omission of Patient Acuity: ", "Disclosures lack electronic health records (EHR) and Case Mix Index (CMI) severity adjustments."),
            ("Single-State Regulatory Boundary: ", "Trained on California HCAI filings; interstate validation requires multi-state federation.")
        ]),
        ("III. Administrative Policy Actions", Inches(8.81), NAVY_LIGHT, [
            ("Peer-Matched Benchmarks: ", "State health agencies must evaluate general acute hospitals against peer clusters, not monolithic averages."),
            ("Buffer Capped-Rate Pressures: ", "Provide targeted rate stabilization for acute facilities with Medicare/Medicaid payer ratios > 65%."),
            ("Subacute Bed Redeployment: ", "Incentivize conversion of underutilized acute beds into subacute recovery and rehab units."),
            ("Specialty Center Oversight: ", "Monitor surgical center expansion to ensure essential trauma and emergency readiness.")
        ])
    ]
    for title, left, col, bullets in tier1_cards:
        _, tf_t1 = add_card_panel(s14, left, Inches(1.25), Inches(3.77), Inches(3.75), title, col)
        for i, (k, v) in enumerate(bullets):
            p = tf_t1.paragraphs[0] if i == 0 else tf_t1.add_paragraph()
            if i > 0:
                p.space_before = Pt(3.5)
            add_run_to_p(p, "• " + k, bold=True, size=Pt(9), color=col)
            add_run_to_p(p, v, size=Pt(8.5), color=TEXT_DARK)

    # Bottom Tier: 2 Wide Future Scope & Technology Transfer Cards (Y=5.12 to 7.00, height 1.88")
    tier2_cards = [
        ("IV. Future Scope: Longitudinal Markov Tracking & Clinical EHR Fusion", Inches(0.75), Inches(5.82), TEAL_DARK, [
            ("Multi-Period Markov Transitions: ", "Extend pipeline to longitudinal 5-year Markov transition matrices to track how facilities migrate between operational clusters over economic and reimbursement cycles."),
            ("Clinical Quality Federation: ", "Federate CMS 30-day readmissions, hospital-acquired infection (HAI) rates, and HCAHPS patient experience scores with financial indicators to model the trade-off between fiscal margins and care outcomes.")
        ]),
        ("V. Technology Transfer: Automated Fiscal Distress Early Warnings", Inches(6.73), Inches(5.82), NAVY, [
            ("Predictive Fiscal Early Warning: ", "Train supervised gradient-boosted classifiers on historical transition labels to detect facilities at imminent risk of slipping into acute fiscal distress 2-4 quarters in advance."),
            ("Multi-State Pipeline Scaling: ", "Scale the data ingestion architecture to federate hospital disclosures across Texas (DSHS), New York (SPARCS), and Florida (AHCA) health agencies for nationwide cross-validation.")
        ])
    ]
    for title, left, w, col, bullets in tier2_cards:
        _, tf_t2 = add_card_panel(s14, left, Inches(5.12), w, Inches(1.88), title, col)
        for i, (k, v) in enumerate(bullets):
            p = tf_t2.paragraphs[0] if i == 0 else tf_t2.add_paragraph()
            if i > 0:
                p.space_before = Pt(3)
            add_run_to_p(p, "• " + k, bold=True, size=Pt(9), color=col)
            add_run_to_p(p, v, size=Pt(8.5), color=TEXT_DARK)

    # Save presentation
    out_dir = os.path.join("presentation")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "CA3_Presentation.pptx")
    prs.save(out_path)
    print(f"Successfully generated updated PowerPoint Presentation: {out_path}")


if __name__ == '__main__':
    build_presentation()
