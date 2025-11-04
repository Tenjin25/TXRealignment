import pandas as pd
from pathlib import Path
p=Path(r"c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TXRealignments\Election_Data\2014_General_Election_Returns.csv")
df=pd.read_csv(p, on_bad_lines='skip')
cols=[c.strip() for c in df.columns]
df.columns=cols
ellis=df[df['County'].str.strip().str.upper()=='ELLIS']
print('Ellis rows:', len(ellis))
print('Unique offices count:', len(ellis['Office'].unique()))
print(ellis['Office'].unique()[:50])
print('--- Offices containing lieutenant ---')
print(ellis[ellis['Office'].str.lower().str.contains('lieutenant', na=False)]['Office'].unique())
print('--- Offices containing lt. ---')
print(ellis[ellis['Office'].str.lower().str.contains('\blt\b', na=False)]['Office'].unique())
