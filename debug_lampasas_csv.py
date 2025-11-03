import pandas as pd
import os

# Check if file exists
file_path = 'Election_Data/20201103__tx__general__county_from_precinct.csv'
print(f"Checking file: {file_path}")
print(f"File exists: {os.path.exists(file_path)}")

if os.path.exists(file_path):
    # Load the file
    df = pd.read_csv(file_path)
    print(f"\nTotal rows: {len(df)}")
    print(f"Unique counties: {df['county'].nunique()}")
    
    # Check for Lampasas
    lampasas = df[df['county'] == 'Lampasas']
    print(f"\nLampasas rows: {len(lampasas)}")
    
    if len(lampasas) > 0:
        print("\nLampasas data:")
        print(lampasas)
        
        # Check Senate race specifically
        senate = lampasas[lampasas['office'] == 'U.S. Senate']
        print(f"\nLampasas U.S. Senate rows: {len(senate)}")
        if len(senate) > 0:
            print(senate)
            print(f"\nTotal Senate votes: {senate['votes'].sum()}")
