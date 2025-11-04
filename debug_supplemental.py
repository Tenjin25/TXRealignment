import pandas as pd
from pathlib import Path
import re

# Test reading the 2000 supplemental file
election_dir = Path("Election_Data")
filepath = election_dir / "20001107__tx__general__county.csv"

print(f"Checking file: {filepath}")
print(f"File exists: {filepath.exists()}")

if filepath.exists():
    print("\nReading CSV...")
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.lower().str.strip()
    
    print(f"Columns: {df.columns.tolist()}")
    print(f"Total rows: {len(df)}")
    
    # Get unique offices
    offices = df['office'].unique()
    print(f"\nTotal unique offices: {len(offices)}")
    
    # Filter for judicial
    judicial_offices = [o for o in offices if pd.notna(o) and isinstance(o, str) and ('Supreme Court' in o or 'Criminal Appeals' in o)]
    print(f"Judicial offices: {len(judicial_offices)}")
    
    for office in judicial_offices:
        print(f"  - {office}")
        
        # Test normalization
        low = office.lower()
        if 'supreme court' in low:
            if 'place' in low:
                place_match = re.search(r'(?:place|pl\.?|p)\s*(\d+)', low)
                if place_match:
                    print(f"    -> Would create contest: supreme_court_place_{place_match.group(1)}")
            elif 'justice' in low:
                print(f"    -> Would create contest: supreme_court_justice")
        elif 'criminal appeals' in low:
            if 'presiding' in low:
                print(f"    -> Would create contest: cca_presiding_judge")
            elif 'place' in low:
                place_match = re.search(r'(?:place|pl\.?|p)\s*(\d+)', low)
                if place_match:
                    print(f"    -> Would create contest: cca_place_{place_match.group(1)}")
            elif 'judge' in low:
                print(f"    -> Would create contest: cca_judge")
