import pandas as pd

# Try reading with different quoting options
try:
    df = pd.read_csv('Election_Data/2024_General_Election_Returns-Aligned.csv', 
                     quotechar='"', skipinitialspace=True)
    
    print('Successfully loaded!')
    print(f'Total rows: {len(df):,}')
    print(f'\nColumns: {list(df.columns)}')
    
    # Strip column names
    df.columns = df.columns.str.strip()
    
    print(f'\nUnique offices:')
    offices = sorted(df['Office'].str.strip().unique())
    for office in offices:
        count = len(df[df['Office'].str.strip() == office])
        print(f'  {office}: {count:,} rows')
    
    # Check for President and US Senate
    president_rows = df[df['Office'].str.contains('President', case=False, na=False)]
    senate_rows = df[df['Office'].str.contains('U.S. Senate', case=False, na=False) | 
                     df['Office'].str.contains('United States Senator', case=False, na=False)]
    
    print(f'\n✓ President rows: {len(president_rows):,}')
    print(f'✓ US Senate rows: {len(senate_rows):,}')
    
    if len(president_rows) > 0:
        print(f'\nPresident candidates: {sorted(president_rows["Name"].str.strip().unique())}')
    
    if len(senate_rows) > 0:
        print(f'\nUS Senate candidates: {sorted(senate_rows["Name"].str.strip().unique())}')
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
