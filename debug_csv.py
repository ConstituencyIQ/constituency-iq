import pandas as pd

print("--- CSV DIAGNOSTIC REPORT ---")
try:
    df = pd.read_csv('constituencies_master.csv')
    print(f"Detected Columns: {list(df.columns)}")
    print(f"Total Rows: {len(df)}")
    print("\nColumn Data Types:")
    print(df.dtypes)
    print("\nFirst Row Raw Data:")
    print(df.iloc[0].to_dict())
except Exception as e:
    print(f"CRITICAL PARSING ERROR: {e}")