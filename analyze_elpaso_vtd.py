import pandas as pd

# Check the VTD CSV in detail
df = pd.read_csv('Election_Data/2018_General_Election_Returns-aligned.csv', on_bad_lines='skip')
df.columns = df.columns.str.strip()

# Strip all string values
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.strip()

print("=" * 80)
print("EL PASO VTD DATA ANALYSIS")
print("=" * 80)

# Get El Paso data
el_paso = df[df['County'].str.upper() == 'EL PASO'].copy()
print(f"\nTotal El Paso rows: {len(el_paso)}")

# Check columns
print(f"\nColumns: {df.columns.tolist()}")

# Check US Senate specifically
us_sen = el_paso[el_paso['Office'].str.contains('Sen', case=False, na=False)]
print(f"\nUS Senate rows: {len(us_sen)}")

if len(us_sen) > 0:
    print("\nFirst few rows:")
    print(us_sen[['County', 'Office', 'Party', 'Votes']].head(10))
    
    print("\nUnique offices:")
    print(us_sen['Office'].unique())
    
    print("\nUnique parties:")
    print(us_sen['Party'].unique())
    
    print("\nVotes by party:")
    print(us_sen.groupby('Party')['Votes'].sum())
    
    # Check data types
    print(f"\nVotes column type: {us_sen['Votes'].dtype}")
    
    # Try to convert votes to numeric
    us_sen['Votes'] = pd.to_numeric(us_sen['Votes'], errors='coerce').fillna(0).astype(int)
    
    print("\nAfter converting to numeric:")
    dem_votes = us_sen[us_sen['Party'].str.upper() == 'D']['Votes'].sum()
    rep_votes = us_sen[us_sen['Party'].str.upper() == 'R']['Votes'].sum()
    other_votes = us_sen[~us_sen['Party'].str.upper().isin(['D','R'])]['Votes'].sum()
    
    print(f"  DEM: {dem_votes:,}")
    print(f"  REP: {rep_votes:,}")
    print(f"  Other: {other_votes:,}")
    print(f"  Total: {dem_votes + rep_votes + other_votes:,}")
