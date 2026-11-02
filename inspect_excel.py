import pandas as pd

excel_path = 'data/constituency_weeklypay.xlsx'
xl = pd.ExcelFile(excel_path)
print("Available sheets:", xl.sheet_names)

# Read the first few rows of the first sheet
df = pd.read_excel(excel_path, sheet_name=0, header=None)
print("--- Row 0 to 4 (Headers) ---")
print(df.iloc[0:6, :8].to_string())