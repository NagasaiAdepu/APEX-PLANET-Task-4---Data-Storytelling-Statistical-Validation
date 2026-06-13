"""Rebuilt hypothesis testing script.

Usage:
  python analysis\hypothesis_test.py [--file PATH]

By default uses D:\APEX\APEX_task_4\ApexPlanet_DataAnalytics_Dataset.xlsx if present.
Saves `analysis/test_results.json` and plots to `presentation/figures/`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns


DEFAULT_DATA_PATH = Path(r"D:/APEX/APEX_task_4/ApexPlanet_DataAnalytics_Dataset.xlsx")


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    if path.suffix.lower() in {".xls", ".xlsx"}:
        return pd.read_excel(path)
    return pd.read_csv(path)


def independent_t_test(a: np.ndarray, b: np.ndarray, equal_var: bool = False):
    stat, pval = stats.ttest_ind(a, b, equal_var=equal_var)
    return float(stat), float(pval)


def chi2_contingency_test(table: pd.DataFrame):
    chi2, p, dof, expected = stats.chi2_contingency(table.values)
    return float(chi2), float(p), int(dof), expected


def run_t_test(df: pd.DataFrame) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if not {"Total_Sales", "Gender"}.issubset(df.columns):
        return out
    sub = df.dropna(subset=["Total_Sales", "Gender"])
    groups = list(sub.groupby("Gender"))
    if len(groups) != 2:
        return out
    name0, g0 = groups[0][0], groups[0][1]
    name1, g1 = groups[1][0], groups[1][1]
    a = g0["Total_Sales"].to_numpy()
    b = g1["Total_Sales"].to_numpy()

    # assumptions
    lev_stat, lev_p = stats.levene(a, b)
    t_stat, t_p = stats.ttest_ind(a, b, equal_var=False)

    # Cohen's d (pooled)
    n1, n2 = len(a), len(b)
    s1, s2 = a.std(ddof=1), b.std(ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)) if n1 + n2 - 2 > 0 else 0.0
    cohens_d = float((a.mean() - b.mean()) / pooled_sd) if pooled_sd > 0 else None

    out = {
        "groups": [str(name0), str(name1)],
        "n": {str(name0): int(n1), str(name1): int(n2)},
        "t_stat": float(t_stat),
        "p_value": float(t_p),
        "levene": {"stat": float(lev_stat), "p": float(lev_p)},
        "cohens_d": cohens_d,
        "means": {str(name0): float(a.mean()), str(name1): float(b.mean())},
        "std": {str(name0): float(s1), str(name1): float(s2)},
    }

    # plot
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x="Gender", y="Total_Sales", data=sub, ax=ax)
    ax.set_title("Total_Sales by Gender")
    fig_path = Path("presentation/figures/total_sales_by_gender.png")
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(fig_path, bbox_inches="tight")
    plt.close(fig)
    out["boxplot"] = str(fig_path)
    return out


def run_chi2(df: pd.DataFrame) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if not {"Category", "City"}.issubset(df.columns):
        return out
    table = pd.crosstab(df["Category"], df["City"])
    if table.size == 0:
        return out
    chi2, p, dof, expected = stats.chi2_contingency(table.values)
    n = int(table.values.sum())
    r, c = table.shape
    cramers_v = float(np.sqrt(chi2 / (n * min(r - 1, c - 1)))) if n > 0 and min(r - 1, c - 1) > 0 else None

    # heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(table, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title("Category vs City (counts)")
    fig_path = Path("presentation/figures/category_city_heatmap.png")
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(fig_path, bbox_inches="tight")
    plt.close(fig)

    out = {
        "chi2": float(chi2),
        "p_value": float(p),
        "dof": int(dof),
        "cramers_v": cramers_v,
        "observed_shape": [int(r), int(c)],
        "heatmap": str(fig_path),
    }
    return out


def save_results(results: Dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Hypothesis testing runner")
    parser.add_argument("--file", "--csv", dest="file", help="CSV/Excel file path")
    parser.add_argument("path", nargs="?", help="positional CSV/Excel path")
    args = parser.parse_args(argv)

    path = Path(args.file or args.path) if (args.file or args.path) else (DEFAULT_DATA_PATH if DEFAULT_DATA_PATH.exists() else None)
    if path is None:
        print("No data file found or provided. Exiting.")
        sys.exit(1)

    print("Using data file:", path)
    df = load_dataset(path)
    print("Loaded shape:", df.shape)

    results: Dict[str, Any] = {"data_path": str(path), "columns": list(df.columns)}

    t = run_t_test(df)
    if t:
        results["t_test"] = t

    c = run_chi2(df)
    if c:
        results["chi2"] = c

    out_json = Path("analysis/test_results.json")
    save_results(results, out_json)
    print("Saved results:", out_json)


if __name__ == "__main__":
    main()
