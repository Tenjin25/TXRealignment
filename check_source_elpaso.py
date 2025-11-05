import pandas as pd

# Check 2018 source CSV
df = pd.read_csv('Data/20181106__tx__general__county.csv')

print("Columns:", df.columns.tolist())
print(f"\nTotal rows: {len(df)}")

# Check for El Paso
ep = df[df['county'].str.upper() == 'EL PASO']
print(f"\nEl Paso rows: {len(ep)}")

if len(ep) > 0:
    print("\nSample El Paso data:")
    print(ep[['county', 'office', 'party', 'votes']].head(20))
    
    # Check US Senate specifically
    us_senate = ep[ep['office'].str.contains('Senate', case=False, na=False)]
    if len(us_senate) > 0:
        print("\nEl Paso U.S. Senate votes:")
        print(us_senate[['county', 'office', 'party', 'candidate', 'votes']])
else:
    print("\n⚠️  NO EL PASO DATA FOUND!")
    print("\nChecking what counties ARE in the file:")
    print(df['county'].unique()[:20])
