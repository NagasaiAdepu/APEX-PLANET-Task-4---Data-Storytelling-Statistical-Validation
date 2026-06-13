# Data Storytelling & Statistical Validation Report

**Executive Summary**
- Objective: Synthesize sales analytics into a clear business narrative and validate key findings statistically.
- Key outcome: No statistically significant difference in order Total_Sales by customer gender or by product Category, but a robust predictive model explains ~83% of variance in log(Total_Sales) using Quantity and Unit_Price.

**Business Context & Objective**
- The dataset (`Sales_Dataset` sheet in the provided Excel) contains 1,000 orders with customer demographics, product, pricing, quantity and order-level Total_Sales. The stakeholder goal is to identify meaningful levers to increase revenue per order and to validate observed differences across customer segments.

**Data & Methods**
- Source: c:\Users\vinit\Downloads\ApexPlanet_DataAnalytics_Dataset.xlsx (sheet: `Sales_Dataset`).
- Preprocessing: parsed dates, removed rows with missing Total_Sales; small amounts of missingness in `Age` (~2%) and `City` (~1.3%).
- Statistical tests applied:
  - Two-sample t-test (Welch) for mean Total_Sales by `Gender`.
  - One-way ANOVA for mean Total_Sales across `Category`.
  - Chi-square test for association between `Category` and high order quantity (>= median).
  - Multiple linear regression (OLS) predicting log(1+Total_Sales) from `Quantity`, `Unit_Price`, and `Age`.

**Descriptive Findings**
- Orders: 1,000 rows; `Total_Sales` distribution is right-skewed (see histogram).
- Median `Quantity` = 5; mean `Unit_Price` ≈ 25,487; mean `Total_Sales` ≈ 139,399.

**Statistical Validation — Tests & Interpretation**

- T-test: `Total_Sales` by Gender
  - Result: t = 0.6826, p = 0.4950
  - Means: Male ≈ 141,807; Female ≈ 136,883
  - Effect size: Cohen's d ≈ 0.043 (negligible)
  - Interpretation: No evidence of a statistically significant difference in order value between male and female customers at conventional significance levels. Practically, gender is not a useful segmentation for predicting order value.

- ANOVA: `Total_Sales` across Product `Category`
  - Result: F ≈ 0.717, p ≈ 0.580
  - Eta-squared ≈ 0.0029 (very small)
  - Interpretation: No significant difference in mean Total_Sales between categories; Category alone explains a negligible share of variance in order value.

- Chi-square: `Category` vs High Quantity (>= median)
  - Result: chi2 ≈ 3.333, p ≈ 0.504; Cramer's V ≈ 0.058 (very small)
  - Interpretation: No meaningful association between product category and whether an order is high-quantity.

- Regression: Predicting log(1+Total_Sales)
  - Model (OLS) predictors: `Quantity`, `Unit_Price`, `Age`
  - Model fit: R-squared ≈ 0.829 (Adjusted R2 ≈ 0.828)
  - Coefficients (95% CI):
    - Intercept ≈ 8.704 (CI 8.579, 8.829)
    - `Quantity`: coef ≈ 0.233 (CI 0.222, 0.244), p < 0.001
    - `Unit_Price`: coef ≈ 0.0000576 (CI 0.0000555, 0.0000597), p < 0.001
    - `Age`: coef ≈ -0.00151 (CI -0.00370, 0.000678), p ≈ 0.176 (not significant)
  - Interpretation: Quantity and Unit_Price are highly significant predictors of order value (log scale). Age is not a significant predictor after adjusting for price and quantity. The model explains ~83% of variance in log(Total_Sales), indicating that these product-level variables are the dominant drivers of order value in this dataset.

**Visualization Interpretations**
- Distribution of Total Sales ([histogram](presentation/figures/hist_total_sales.png)):
  - Shows right-skew with a long tail of high-value orders. Median order value is substantially lower than mean, indicating a small set of high-value orders inflates the average.

- Total Sales by Category ([boxplot](presentation/figures/box_total_by_category.png)):
  - Boxplots show similar medians across categories and overlapping distributions, consistent with ANOVA results (no significant differences).

- Total Sales vs Unit Price ([scatter](presentation/figures/scatter_total_unitprice.png)):
  - Positive relationship between unit price and total sale, reinforced by regression. Clustering by `Category` suggests different product mixes but not consistently different order values.

**Business Insights & Implications**
- Primary drivers of order value are product-level: `Unit_Price` and `Quantity`. Efforts to increase average order value should prioritize pricing strategy, product mix, and encouraging larger basket sizes (bundles, volume discounts), rather than targeting customers by gender or product category alone.
- High-value tail: a small fraction of orders drive a disproportionate share of revenue. Identify and profile high-value orders (products, customer segments, purchase channels) for targeted promotions and retention.

**Actionable Recommendations (prioritized)**
1. High Impact / High Feasibility — Increase average order value
   - Implement product bundling and volume discounts targeted at customers with mid-to-high historical purchase quantities.
   - Test value-based pricing or targeted upsell prompts on product pages for higher Unit_Price items.
   - Metric to track: average order value (AOV), median order value, % orders > X.

2. Medium Impact — Target high-value orders and retention
   - Create a loyalty/retention program focused on customers generating high lifetime value.
   - Run a cohort analysis on repeat high-value buyers to identify common attributes (product combination, purchase cadence).

3. Low Impact / Investigate — Segmentation by demographics
   - Avoid aggressive gender-based targeting for AOV uplift; current evidence suggests little to no difference.
   - Consider more granular segmentation (purchase history, product affinity, RFM) rather than demographic splits.

**Suggested Tests & Next Steps**
- Run A/B tests for bundling vs. standard pricing to measure causal uplift in AOV; use t-tests on lift with pre-specified power and sampling.
- Investigate drivers of the high-value tail: build a classification model (e.g., gradient boosting) to predict high-value orders and validate with cross-validation.
- Expand regression to include channel, promotion flags, and customer LTV where available; test interaction terms (e.g., Unit_Price x Category).

**Limitations & Assumptions**
- Observational dataset: causality cannot be inferred without randomized experiments.
- Data quality: small missingness in `Age` and `City`. Analyses assume missingness is random; if not, results may be biased.
- Measurement: `Unit_Price` and `Quantity` are per-order; if discounts or returns are not captured, Total_Sales may misstate realized revenue.

**Artifacts & Files**
- Analysis script: [analysis/hypothesis_test.py](analysis/hypothesis_test.py#L1)
- Saved statistical results: [analysis/stat_results.json](analysis/stat_results.json#L1)
- Figures: [presentation/figures/box_total_by_category.png](presentation/figures/box_total_by_category.png), [presentation/figures/hist_total_sales.png](presentation/figures/hist_total_sales.png), [presentation/figures/scatter_total_unitprice.png](presentation/figures/scatter_total_unitprice.png)

If you'd like, I can:
- Convert this report into a concise PowerPoint (7–10 slides) highlighting the executive summary and recommended tests.
- Prepare pre-approved A/B test designs for bundling or upsell experiments (sample size and test length).

---
_Report generated programmatically. For detailed numbers and model output see the saved `analysis/stat_results.json` and the regression summary included there._
