# Final Project Submission Checklist — CA3 Machine Learning Mini-Project
**Project Title:** Healthcare Facility Financial and Resource Utilization Pattern Analysis Using Machine Learning  
**Student / Candidate:** Aditya09977  
**Submission Deadline:** 24 October 2026, 8:00 PM  

---

## Deliverables Status Tracker

| Deliverable Item | Target File Location | Requirement Status | Verification Notes |
| :--- | :--- | :---: | :--- |
| **1. IEEE Research Report** | `report/IEEE_Report.docx` | **COMPLETE** | Full 6-page conference format in DOCX (~867 KB), complete with equations, tables, embedded figures, and 15 IEEE citations. |
| **2. IEEE LaTeX Source Package** | `report/IEEE_LaTeX_Source.zip` | **COMPLETE** | Contains `main.tex`, `references.bib`, and all embedded figures in `figures/`. |
| **3. PowerPoint Presentation** | `presentation/CA3_Presentation.pptx` | **COMPLETE** | 14 professional slides (~1.1 MB) in 16:9 widescreen format with actual metrics, charts, and diagrams. |
| **4. Clean GitHub-Ready Codebase** | `src/`, `scripts/`, `app.py` | **COMPLETE** | Modular Python code with `preprocessing.py`, `clustering.py`, `evaluation.py`, and `run_experiments.py`. |
| **5. Streamlit Analytics Dashboard** | `app.py` | **COMPLETE** | Interactive 6-section analytics application with 2D PCA cluster visualization, search, and CSV download. |
| **6. Jupyter Notebook** | `healthcare_analysis.ipynb` | **COMPLETE** | Step-by-step exploratory data analysis, feature engineering, and model validation workflow. |
| **7. Raw & Processed Data** | `data/raw/`, `data/processed/` | **COMPLETE** | Genuine source filings (2,192 records across 5 quarters) and 428 cleaned annual facility profiles. |
| **8. Experimental Results** | `results/experiment_results.csv` | **COMPLETE** | 64 benchmarked experimental runs across K-Means, Agglomerative (Ward/Avg/Comp), and DBSCAN. |
| **9. Cluster Profiles** | `results/cluster_profiles.csv` | **COMPLETE** | Quantitative medians and deviations for all 4 discovered facility archetypes. |
| **10. Literature Review Matrix** | `docs/literature_review.csv` | **COMPLETE** | 15 verified peer-reviewed research papers (2021–2026) with DOIs, objectives, methods, and project relevance. |
| **11. Publication Diagrams** | `figures/`, `docs/diagrams/` | **COMPLETE** | Architecture diagram, preprocessing pipeline, clustering workflow, elbow curve, PCA scatter, and profile comparisons. |
| **12. Plagiarism Checklist** | `docs/PLAGIARISM_CHECKLIST.md` | **COMPLETE** | Detailed protocol for `<10%` similarity and `<20%` AI thresholds with institutional scoring sheet. |
| **13. Requirements & Git Ignore** | `requirements.txt`, `.gitignore` | **COMPLETE** | Specific, maintained library versions with zero cloud/heavy framework bloat. |
| **14. Master README** | `README.md` | **COMPLETE** | Project documentation, mathematical formulation, reproduction commands, and viva preparation Q&A. |

---

## Verification of Execution Commands
- [x] `pip install -r requirements.txt` (Installs pandas, numpy, scikit-learn, matplotlib, seaborn, streamlit, python-docx, python-pptx)
- [x] `python scripts/run_experiments.py` (Executes end-to-end data processing, 64 clustering experiments, and generates figures)
- [x] `python scripts/generate_diagrams.py` (Compiles all architecture and workflow diagrams)
- [x] `python scripts/generate_ieee_report.py` (Builds `report/IEEE_Report.docx`)
- [x] `python scripts/generate_presentation.py` (Builds `presentation/CA3_Presentation.pptx`)
- [x] `python scripts/generate_latex_source.py` (Packages `report/IEEE_LaTeX_Source.zip`)
- [x] `streamlit run app.py` (Launches interactive web dashboard on `localhost:8501`)
