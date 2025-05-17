import numpy as np
import pandas as pd

def initial_report(df):
    print(" *** DATA CLEANING CHECKLIST ***\n" + "-"*40)

    print(f"*** Structure:\n- Total Rows: {df.shape[0]}\n- Total Columns: {df.shape[1]}")
    print(f"- Column Names: {list(df.columns)}\n")

    
    print("📌 Data Types:")
    for col, dtype in df.dtypes.items():
        print(f"  {col}: {dtype}")
    print()

    print("🧬 Mixed Data Types:")
    for col in df.columns:
        try:
            type_counts = df[col].apply(type).value_counts()
            if len(type_counts) > 1:
                print(f"  {col}:")
                for t, count in type_counts.items():
                    print(f"    - {t.__name__}: {count}")
        except Exception as e:
            print(f"  {col}: Error checking types - {e}")
    print()

    print("*** Distinct Values per Column:")
    for col in df.columns:
        print(f"  {col}: {df[col].nunique()}")
    print()

    print("*** Null Values and Percentages:")
    nulls = df.isnull().sum()
    for col in df.columns:
        pct_missing = np.mean(df[col].isnull())
        if nulls[col] > 0: # Only print if there are missing values
            print(f"  {col}: Missing Values: {nulls[col]}, Pct: {round(pct_missing * 100, 3)}%")
    print()

    
    print(f"\n*** Duplicates: {df.duplicated().sum()}")
    constant_cols = df.columns[df.nunique() == 1].tolist()
    if constant_cols:
        print(f"🧱 Constant Columns (no variance): {constant_cols}")
    print()

    print("*** Negative or Zero Values:")
    for col in df.select_dtypes(include='number').columns:
        count = (df[col] <= 0).sum()
        if count > 0:
            print(f"  {col}: {count}")
    print()


    print("*** Basic Statistics:")
    stat=df.describe()
    print(f"{stat}\n")

    print("*** Category Description:")
    stat=df.describe(include='O')
    print(f"{stat}\n")
    
    print("*** Outliers (IQR method):")
    for col in df.select_dtypes(include='number').columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        if not outliers.empty:
            print(f"  {col}: {len(outliers)} outliers")
            print(f"    Lower Bound: {lower_bound:.2f}")  # Limiting to 2 decimal places for display
            print(f"    Upper Bound: {upper_bound:.2f}")  # Limiting to 2 decimal places for display
        else:
            print(f"  {col}: No outliers")
            print(f"    Lower Bound: {lower_bound:.2f}")
            print(f"    Upper Bound: {upper_bound:.2f}")
    print("-" * 40)