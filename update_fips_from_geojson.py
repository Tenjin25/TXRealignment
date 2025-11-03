import json
import csv

# Read the GeoJSON file
print("Reading GeoJSON file from Census...")
with open('TX_Data/tl_2020_48_county20/tl_2020_48_county20.geojson', 'r') as f:
    geojson_data = json.load(f)

# Extract FIPS and county names
fips_mapping = []

for feature in geojson_data['features']:
    props = feature['properties']
    geoid = props.get('GEOID20')  # Census 2020 GeoJSON uses GEOID20
    name = props.get('NAME20')     # Census 2020 GeoJSON uses NAME20
    
    if geoid and name:
        fips_mapping.append({
            'fips': geoid,
            'county': name
        })

# Sort by FIPS code
fips_mapping.sort(key=lambda x: x['fips'])

# Write to CSV
print(f"\nWriting {len(fips_mapping)} counties to texas_county_fips.csv...")
with open('TX_Data/texas_county_fips.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['fips', 'county'])
    writer.writeheader()
    writer.writerows(fips_mapping)

print("✅ FIPS mapping updated from Census GeoJSON")

# Verify Lampasas specifically
lampasas = [x for x in fips_mapping if x['fips'] == '48281']
if lampasas:
    print(f"\n✓ FIPS 48281 now maps to: {lampasas[0]['county']}")
else:
    print(f"\n⚠️ FIPS 48281 not found in GeoJSON")

# Show sample
print(f"\nSample mappings:")
for item in fips_mapping[:10]:
    print(f"  {item['fips']}: {item['county']}")
