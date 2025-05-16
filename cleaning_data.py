# cleaning_utils.py

import pandas as pd
import re

# 1. Clean numeric columns (removes $, %, commas, letters)
def clean_numeric_column(df, col):
    print(f"[clean_numeric_column] Cleaning column: {col}")
    before_na = df[col].isna().sum()
    before_clean=pd.to_numeric(df[col], errors='coerce').isna().sum()
    df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
    df[col] = pd.to_numeric(df[col], errors='coerce')
    after_na = df[col].isna().sum()
    after_clean=pd.to_numeric(df[col], errors='coerce').isna().sum()
    print(f"[clean_numeric_column] [NaNs before: {before_na}, after: {after_na}];"
          f" [Problems before: {before_clean}, after:{after_clean}]")
    return df

# 2. Standardize text columns (strip, lowercase)
def clean_text_column(df, col):
    print(f"[clean_text_column] Standardizing column: {col}")
    df[col] = df[col].astype(str).str.strip().str.lower()
    return df

# 3. Fix category typos using a mapping dict
def correct_categories(df, col, mapping_dict):
    print(f"[correct_categories] Correcting values in column: {col}")
    unique_before = df[col].unique()
    df[col] = df[col].replace(mapping_dict)
    unique_after = df[col].unique()
    print(f"[correct_categories] Unique values before: {unique_before}")
    print(f"[correct_categories] Unique values after: {unique_after}")
    return df

# 4. Convert string to datetime safely
def convert_to_datetime(df, col, format=None):
    print(f"[convert_to_datetime] Converting to datetime: {col}")
    df[col] = pd.to_datetime(df[col], format=format, errors='coerce')
    null_count = df[col].isna().sum()
    print(f"[convert_to_datetime] Null values after conversion: {null_count}")
    return df

# 5. Drop duplicate rows
def drop_duplicates(df):
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    print(f"[drop_duplicates] Dropped {before - after} duplicate rows")
    return df

# 6. Report missing values
def missing_value_report(df):
    print("[missing_value_report] Generating missing value report...")
    report = df.isnull().sum().sort_values(ascending=False)
    print(report[report > 0])
    return report

# 7. Fill missing values (can specify method or value)
def fill_missing(df, col, method='mean', value=None):
    print(f"[fill_missing] Filling missing values in column: {col}")
    before_na = df[col].isna().sum()
    if value is not None:
        df[col] = df[col].fillna(value)
        method_used = f"filled with constant value: {value}"
    elif method == 'mean':
        df[col] = df[col].fillna(df[col].mean())
        method_used = "mean"
    elif method == 'median':
        df[col] = df[col].fillna(df[col].median())
        method_used = "median"
    elif method == 'mode':
        df[col] = df[col].fillna(df[col].mode()[0])
        method_used = "mode"
    after_na = df[col].isna().sum()
    print(f"[fill_missing] {method_used} → NaNs before: {before_na}, after: {after_na}")
    return df

# 8. Trim all string columns
def trim_all_str_columns(df):
    print("[trim_all_str_columns] Trimming whitespace in all string columns...")
    str_cols = df.select_dtypes(include='object').columns
    for col in str_cols:
        print(f" - Trimming column: {col}")
        df[col] = df[col].str.strip()
    return df


# 9. drop duplicate primary
def drop_duplicate_primary(df, primary_col, keep='first'):
    """
    Drops rows where the primary column has duplicate values.

    Parameters:
    - df: DataFrame
    - primary_col: Column name to check for uniqueness (e.g., 'user_id')
    - keep: 'first' (default), 'last', or False — same as pandas' drop_duplicates

    Returns:
    - Cleaned DataFrame with duplicates in primary_col removed.
    """
    before = df.shape[0]
    df = df.drop_duplicates(subset=[primary_col], keep=keep)
    after = df.shape[0]
    print(f"[drop_duplicate_primary] Dropped {before - after} rows with duplicate {primary_col}")
    return df

# 10. check_column_types
def check_column_types(df):
    """
    Checks data type consistency within each column of the DataFrame.
    Flags columns that contain mixed types.

    Parameters:
    - df: pandas DataFrame

    Returns:
    - A summary DataFrame showing type breakdown per column
    """
    report = []

    for col in df.columns:
        type_counts = df[col].apply(type).value_counts()
        type_info = {str(t.__name__): c for t, c in type_counts.items()}
        report.append({
            'column': col,
            'types_found': type_info,
            'num_types': len(type_info),
            'is_mixed': len(type_info) > 1
        })

    return pd.DataFrame(report)
