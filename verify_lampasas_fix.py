import pandas as pd

# Read the newly generated county file
df = pd.read_csv('Election_Data/20201103__tx__general__county_from_precinct.csv')

# Filter for Lampasas County
lampasas = df[df['county'] == 'Lampasas']

# Filter for Senate race
senate = lampasas[lampasas['office'] == 'US Senate']

print("Lampasas County 2020 Senate Results:")
print("="*60)
print(senate[['county', 'office', 'party', 'candidate', 'votes']].to_string(index=False))
print("="*60)
print(f"\nTotal votes: {senate['votes'].sum()}")

# Also check if there's any data under "Lamb" county now
lamb = df[df['county'] == 'Lamb']
lamb_senate = lamb[lamb['office'] == 'US Senate']
print(f"\n\nLamb County 2020 Senate Results:")
print("="*60)
if len(lamb_senate) > 0:
    print(lamb_senate[['county', 'office', 'party', 'candidate', 'votes']].to_string(index=False))
    print("="*60)
    print(f"Total votes: {lamb_senate['votes'].sum()}")
else:
    print("(No data found - this is expected)")
