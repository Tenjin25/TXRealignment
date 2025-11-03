import pandas as pd
from pathlib import Path

csv_path = Path(r"Election_Data/2024_General_Election_Returns.csv")

def normalize_office_name(office_name):
    if pd.isna(office_name):
        return ''
    s = str(office_name).strip()
    low = s.lower()
    if 'president' in low:
        return 'President'
    if ('u.s.' in low or 'us ' in low or low.startswith('u.s') or low.startswith('us')) and 'sen' in low:
        return 'U.S. Senate'
    if 'governor' in low:
        return 'Governor'
    if 'lieutenant' in low and 'governor' in low:
        return 'Lieutenant Governor'
    if 'attorney general' in low:
        return 'Attorney General'
    if 'comptroller' in low:
        return 'Comptroller'
    if 'agriculture' in low:
        return 'Agriculture Commissioner'
    if 'railroad' in low:
        return 'Railroad Commissioner'
    return s


df = pd.read_csv(csv_path)
unique_offices = sorted(df['Office'].dropna().unique())
print("Found unique office labels (sample up to 50):")
for o in unique_offices[:50]:
    print("  ", repr(o))

# Show normalized mapping counts
mapping = {}
for o in unique_offices:
    norm = normalize_office_name(o)
    mapping.setdefault(norm, 0)
    mapping[norm] += len(df[df['Office'] == o])

print('\nNormalized office mapping (name -> number of rows in CSV):')
for k, v in sorted(mapping.items()):
    print(f"  {k!r:25} -> {v}")

# Show a few examples of U.S. Senate rows
us_sen_rows = df[df['Office'].str.contains('Sen', na=False, case=False)].head(10)
print('\nExample rows (Office contains "Sen"):\n')
print(us_sen_rows[['County','Office','Name','Party','Votes']].to_string(index=False))
