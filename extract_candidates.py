import pandas as pd

# Extract 2022 candidates
df_2022 = pd.read_csv('Election_Data/20221108__tx__general__precinct.csv')
contests_2022 = ['Governor', 'Lieutenant Governor', 'Attorney General', 'Comptroller of Public Accounts']

print("=== 2022 CANDIDATES ===")
for contest in contests_2022:
    print(f"\n{contest}:")
    candidates = df_2022[df_2022['office'] == contest][['party', 'candidate']].drop_duplicates().sort_values('party')
    for _, row in candidates.iterrows():
        print(f"  {row['party']}: {row['candidate']}")

# Extract 2020 candidates
df_2020 = pd.read_csv('Election_Data/20201103__tx__general__precinct.csv')
contests_2020 = ['President', 'U.S. Senate']

print("\n\n=== 2020 CANDIDATES ===")
for contest in contests_2020:
    print(f"\n{contest}:")
    candidates = df_2020[df_2020['office'] == contest][['party', 'candidate']].drop_duplicates().sort_values('party')
    for _, row in candidates.iterrows():
        print(f"  {row['party']}: {row['candidate']}")
