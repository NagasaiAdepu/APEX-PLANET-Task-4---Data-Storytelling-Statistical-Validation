# Task 4 — Data Storytelling & Statistical Validation

Objective
- Synthesize analysis into a clear business narrative and validate key findings using basic statistical methods.

Structure
- `analysis/` — data analysis and hypothesis testing scripts.
- `presentation/` — slides and speaker notes (placeholders).
- `requirements.txt` — Python deps for analysis.

How to use
1. Create a virtual environment and install deps:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Run the example hypothesis tests (uses synthetic data if no CSV provided):

   ```powershell
   python analysis/hypothesis_test.py
   ```

What to deliver
- Final presentation deck (PowerPoint/Google Slides) with clear objective, analysis, conclusions, and call to action.
- Hypothesis testing summary (one-page): tests run, p-values, confidence intervals, business conclusion.
- Optional: 7–10 minute stakeholder video summarizing insights.

Notes
- See `analysis/hypothesis_test.py` for test utilities and examples.
