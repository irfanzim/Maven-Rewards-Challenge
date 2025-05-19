import pandas as pd


def check_outlier(df, column, show_summary=True):
    """
    Detects and displays outliers in a DataFrame column using the IQR method.

    Parameters:
        df (pd.DataFrame): Input DataFrame
        column (str): Column name to check for outliers
        show_summary (bool): Whether to print IQR, bounds, etc.

    Returns:
        pd.DataFrame: Rows in df where outliers are detected in the specified column
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers_df = df[(df[column] < lower_bound) | (df[column] > upper_bound)].copy()
    outliers_df["outlier_flag"] = "yes"

    if show_summary:
        print(f"📊 Outlier Summary for `{column}`:")
        print("-" * 40)
        print(f"Q1 (25th percentile): {Q1:.2f}")
        print(f"Q3 (75th percentile): {Q3:.2f}")
        print(f"IQR (Q3 - Q1): {IQR:.2f}")
        print(f"Lower bound: {lower_bound:.2f}")
        print(f"Upper bound: {upper_bound:.2f}")
        print(f"Number of outliers: {len(outliers_df)}")
        print("-" * 40)

    return outliers_df
