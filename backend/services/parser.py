"""
parser.py — Turn a raw CSV/XLSX upload into a concise textual summary
that can be fed to an LLM without hitting token limits.
"""
import io
import pandas as pd


def parse_file(file_like: io.BytesIO, ext: str) -> str:
    """
    Read a CSV or XLSX file and produce a compact text representation.

    Returns a string containing:
    - Column names and dtypes
    - Shape (rows × columns)
    - First 10 rows as a markdown table
    - Numeric aggregate statistics (sum / mean / max per column)
    """
    if ext == ".csv":
        df = pd.read_csv(file_like)
    elif ext == ".xlsx":
        df = pd.read_excel(file_like, engine="openpyxl")
    else:
        raise ValueError(f"Unsupported extension: {ext}")

    lines = []

    # --- Basic info ---
    lines.append(f"**Dataset shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    lines.append("")

    # --- Column overview ---
    lines.append("**Columns:**")
    for col in df.columns:
        lines.append(f"  - {col} ({df[col].dtype})")
    lines.append("")

    # --- Sample rows (up to 10) ---
    lines.append("**Sample data (first 10 rows):**")
    lines.append(df.head(10).to_markdown(index=False))
    lines.append("")

    # --- Numeric aggregates ---
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        agg = df[numeric_cols].agg(["sum", "mean", "max", "min"]).round(2)
        lines.append("**Numeric aggregates (sum / mean / max / min):**")
        lines.append(agg.to_markdown())
        lines.append("")

    # --- Categorical value counts ---
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    for col in cat_cols[:5]:  # limit to first 5 categorical columns
        vc = df[col].value_counts().head(10)
        lines.append(f"**Top values in '{col}':**")
        lines.append(vc.to_markdown())
        lines.append("")

    return "\n".join(lines)
