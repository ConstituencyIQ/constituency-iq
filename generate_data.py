import pandas as pd
import json
import os

def process_earnings_data():
    # Point directly to your clean full-time spreadsheet in the root project folder
    excel_path = 'data/constituency_weeklypay.xlsx'
    
    if not os.path.exists(excel_path):
        print(f"Error: Could not find {excel_path} in the root directory.")
        return

    df = pd.read_excel(excel_path, sheet_name=0, header=None)
    
    earnings_map = {}
    uk_median = 811.20  # Official UK full-time median benchmark
    
    for _, row in df.iterrows():
        desc = str(row[0]).strip() if pd.notna(row[0]) else ""
        code = str(row[1]).strip().replace("'", "") if pd.notna(row[1]) else ""
        
        if not code:
            continue
            
        # Capture UK National Benchmark
        if code == 'K02000001' or desc.lower() == 'united kingdom':
            val = row[3]
            if pd.notna(val):
                try:
                    uk_median = float(val)
                except ValueError:
                    pass
            continue

        # STRICT GEOGRAPHY FILTER: Only accept Parliamentary Constituency codes 
        # (E14 = England, S14 = Scotland, W07 = Wales, N15 = Northern Ireland)
        if not code.startswith(('E14', 'S14', 'W07', 'N15')):
            continue
            
        # Column 3 = Median Weekly Pay, Column 4 = Annual Change
        median_val = row[3]
        if pd.notna(median_val):
            try:
                val_float = float(median_val)
                annual_change = float(row[4]) if len(row) > 4 and pd.notna(row[4]) else None
                
                earnings_map[code] = {
                    "constituency": desc,
                    "medianWeeklyPay": val_float,
                    "annualChange": annual_change
                }
            except ValueError:
                continue

    print(f"Successfully parsed {len(earnings_map)} constituencies. UK Full-Time Median: £{uk_median}")

    # Inject precisely into individual constituency JSON files in public/ matching by ONS code
    public_dir = 'public'
    updated_count = 0
    if os.path.exists(public_dir):
        for filename in os.listdir(public_dir):
            if filename.endswith('.json') and filename != 'constituencies-index.json':
                filepath = os.path.join(public_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        c_data = json.load(f)
                    
                    # Match by ONS code (onsCode or id)
                    c_code = c_data.get('onsCode') or c_data.get('id') or c_data.get('code')
                    
                    match = earnings_map.get(c_code)
                    if match:
                        c_data['wage'] = {
                            "medianWeeklyPay": match['medianWeeklyPay'],
                            "annualChange": match['annualChange'],
                            "ukPay": uk_median
                        }
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(c_data, f, indent=2)
                        updated_count += 1
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    
        print(f"Successfully injected verified full-time wage data into {updated_count} constituency JSON files.")

if __name__ == '__main__':
    process_earnings_data()