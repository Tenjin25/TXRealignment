import csv

# Read CSV with basic CSV module to avoid pandas parsing issues
offices = set()

try:
    with open('Election_Data/2020_General_Election_Returns-aligned.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Find the Office column (it might have spaces)
            for key in row.keys():
                if 'Office' in key:
                    office = row[key].strip()
                    if office:
                        offices.add(office)
                    break
except Exception as e:
    print(f"Error: {e}")

print("Unique offices in 2020 aligned CSV:")
for office in sorted(offices):
    print(f"  - {office}")

print(f"\nTotal: {len(offices)} offices")
