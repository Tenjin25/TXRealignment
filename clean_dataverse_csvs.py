"""
Clean and standardize dataverse CSV files to match OpenElections format.
Converts dataverse format to simple county-level format with columns:
county, office, party, candidate, votes
"""

import pandas as pd
from pathlib import Path

def clean_dataverse_csv(input_path, output_path, year):
    """
    Clean a dataverse CSV and convert to OpenElections format
    """
    print(f"\nProcessing {year} dataverse CSV...")
    print(f"  Input: {input_path}")
    
    # Read the dataverse CSV
    df = pd.read_csv(input_path, low_memory=False)
    
    print(f"  Original rows: {len(df):,}")
    print(f"  Original columns: {len(df.columns)}")
    
    # Standardize column names
    df.columns = df.columns.str.strip()
    
    # Select and rename columns to match OpenElections format
    result = pd.DataFrame()
    result['county'] = df['county_name']
    result['office'] = df['office']
    result['party'] = df['party_simplified']
    result['candidate'] = df['candidate']
    result['votes'] = pd.to_numeric(df['votes'], errors='coerce').fillna(0).astype(int)
    
    # Normalize party names to standard abbreviations
    party_map = {
        'REPUBLICAN': 'REP',
        'DEMOCRAT': 'DEM',
        'LIBERTARIAN': 'LIB',
        'GREEN': 'GRN',
        'OTHER': 'OTH'
    }
    result['party'] = result['party'].map(lambda x: party_map.get(str(x).strip().upper(), str(x).strip().upper()) if pd.notna(x) else x)
    
    # Aggregate from precinct to county level (sum votes by county/office/party/candidate)
    print(f"  Aggregating precinct data to county level...")
    result = result.groupby(['county', 'office', 'party', 'candidate'], dropna=False).agg({
        'votes': 'sum'
    }).reset_index()
    
    # Clean up county names (title case, strip whitespace)
    result['county'] = result['county'].str.strip().str.title()
    
    # Normalize office names to match expected values in processor
    office_map = {
        'US PRESIDENT': 'President',
        'US SENATE': 'U.S. Senate',
        'US HOUSE': 'U.S. House',
        'RAILROAD COMMISSIONER': 'Railroad Commissioner',
        'STATE SUPREME COURT JUSTICE': 'Supreme Court Justice',
        'COURT OF CRIMINAL APPEALS': 'Court of Criminal Appeals',
        'COURT OF CRIMINAL APPEALS PRESIDING JUDGE': 'Presiding Judge, Court of Criminal Appeals',
        'STATE BOARD OF EDUCATION': 'State Board of Education',
        'STATE SENATE': 'State Senate',
        'STATE HOUSE': 'State House',
        'COURT OF APPEALS': 'Court of Appeals'
    }
    result['office'] = result['office'].str.strip().str.upper()
    result['office'] = result['office'].map(lambda x: office_map.get(x, x.title()) if pd.notna(x) else x)
    
    # Clean up candidate names (strip whitespace)
    result['candidate'] = result['candidate'].str.strip()
    
    # Sort by county, office, party for consistency
    result = result.sort_values(['county', 'office', 'party', 'candidate'])
    
    print(f"  Final rows: {len(result):,}")
    print(f"  Counties: {result['county'].nunique()}")
    print(f"  Offices: {result['office'].nunique()}")
    
    # Save to CSV
    result.to_csv(output_path, index=False)
    print(f"  ✓ Saved to: {output_path}")
    
    # Show sample
    print(f"\n  Sample data:")
    print(result.head(10).to_string(index=False))
    
    return result

def main():
    """Clean both 2022 and 2024 dataverse CSVs"""
    
    print("=" * 80)
    print("Dataverse CSV Cleaner")
    print("Converting dataverse format to OpenElections county-level format")
    print("=" * 80)
    
    election_dir = Path("Election_Data")
    
    # Clean 2022 data
    clean_dataverse_csv(
        input_path=election_dir / "2022-tx-local-precinct-general" / "TX-cleaned.csv",
        output_path=election_dir / "20221108__tx__general__county.csv",
        year=2022
    )
    
    # Clean 2024 data
    clean_dataverse_csv(
        input_path=election_dir / "tx24" / "tx24.csv",
        output_path=election_dir / "20241105__tx__general__county.csv",
        year=2024
    )
    
    print("\n" + "=" * 80)
    print("✅ Cleaning complete!")
    print("=" * 80)
    print("\nCleaned files created:")
    print("  - Election_Data/20221108__tx__general__county.csv")
    print("  - Election_Data/20241105__tx__general__county.csv")
    print("\nThese files are now in OpenElections format with columns:")
    print("  county, office, party, candidate, votes")

if __name__ == "__main__":
    main()
