import csv
import json

print("Processing official constituency dataset with pure Python CSV reader...")

count = 0
# Open the CSV file safely with UTF-8 encoding
with open('constituencies_master.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    
    # Read the header row and print it for absolute verification
    header = next(reader)
    print(f"CSV Headers detected: {header}")
    
    for row_idx, row in enumerate(reader):
        if not row:
            continue  # Skip empty rows
            
        print(f"Processing row {row_idx}: {row[0]} ({row[4]})")
        
        # Explicit positional unpacking (Guaranteed index mapping)
        # 0: name, 1: region, 2: slug, 3: onsCode, 4: electorate
        name = row[0].strip()
        region = row[1].strip()
        slug = row[2].strip()
        ons_code = row[3].strip()
        
        # Clean electorate string (removes commas, spaces)
        electorate_clean = row[4].replace(",", "").strip()
        
        seat_record = {
            "name": name,
            "region": region,
            "onsCode": ons_code,
            "electorate": int(electorate_clean),
            "metrics": {
                "medianEarnings": row[5].strip(),
                "earningsVariance": row[6].strip(),
                "housePrice": row[7].strip(),
                "housePriceVariance": row[8].strip(),
                "claimantRate": row[9].strip(),
                "claimantVariance": row[10].strip(),
                "crimeRate": row[11].strip(),
                "crimeVariance": row[12].strip()
            }
        }
        
        output_path = f"public/{slug}.json"
        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(seat_record, outfile, indent=4)
            
        count += 1

print(f"Success! Generated {count} official constituency data files.")