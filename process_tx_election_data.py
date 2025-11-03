import pandas as pd
import json
import os
from pathlib import Path
from collections import defaultdict

def normalize_county_name(name):
    """Normalize county name for consistent matching"""
    if pd.isna(name):
        return ""
    return str(name).upper().strip()

def aggregate_single_precinct_file(filepath, year):
    """
    Aggregate a single precinct-level CSV file to county-level data
    (for files like 20221108__tx__general__precinct.csv)
    """
    print(f"  Aggregating single precinct file for {year}...")
    
    try:
        df = pd.read_csv(filepath)
        
        # Ensure county column exists
        if 'county' not in df.columns:
            print(f"  Warning: No 'county' column in {filepath}")
            return None
        
        # Aggregate to county level
        # Group by county, office, and candidate/party
        agg_data = df.groupby(['county', 'office', 'candidate', 'party'], dropna=False).agg({
            'votes': 'sum'
        }).reset_index()
        
        print(f"  Aggregated {len(df['county'].unique())} counties")
        return agg_data
        
    except Exception as e:
        print(f"  Error: Could not process {filepath}: {e}")
        return None

def aggregate_precinct_to_county(precinct_dir, year):
    """
    Aggregate precinct-level CSV files to county-level data
    Returns a DataFrame similar to county-level CSV structure
    """
    print(f"  Aggregating precinct directory for {year}...")
    
    all_data = []
    precinct_files = list(Path(precinct_dir).glob("*__precinct.csv"))
    
    if not precinct_files:
        print(f"  No precinct files found in {precinct_dir}")
        return None
    
    for precinct_file in precinct_files:
        try:
            df = pd.read_csv(precinct_file)
            
            # Extract county name from filename
            # Format: YYYYMMDD__tx__general__COUNTYNAME__precinct.csv
            filename = precinct_file.stem
            parts = filename.split('__')
            if len(parts) >= 4:
                county_name = parts[3].replace('_', ' ').upper()
                df['county'] = county_name
                all_data.append(df)
        except Exception as e:
            print(f"  Warning: Could not process {precinct_file.name}: {e}")
            continue
    
    if not all_data:
        return None
    
    # Combine all precinct data
    combined = pd.concat(all_data, ignore_index=True)
    
    # Aggregate to county level
    # Group by county, office, and candidate/party
    agg_data = combined.groupby(['county', 'office', 'candidate', 'party'], dropna=False).agg({
        'votes': 'sum'
    }).reset_index()
    
    print(f"  Aggregated {len(precinct_files)} counties")
    return agg_data

def get_competitiveness_color(category, party):
    """Get the hex color for a given competitiveness category and party"""
    color_map = {
        "Republican": {
            "Annihilation": "#67000d",
            "Dominant": "#a50f15",
            "Stronghold": "#cb181d",
            "Safe": "#ef3b2c",
            "Likely": "#fb6a4a",
            "Lean": "#fcae91",
            "Tilt": "#fee8c8"
        },
        "Democratic": {
            "Annihilation": "#08306b",
            "Dominant": "#08519c",
            "Stronghold": "#3182bd",
            "Safe": "#6baed6",
            "Likely": "#9ecae1",
            "Lean": "#c6dbef",
            "Tilt": "#e1f5fe"
        },
        "Tossup": "#f7f7f7"
    }
    
    if party == "Tossup":
        return color_map["Tossup"]
    
    return color_map.get(party, {}).get(category, "#cccccc")

def process_texas_election_data():
    """
    Process Texas election CSV files and create a JSON structure
    similar to the NC map format
    """
    
    # Base directory for election data
    election_dir = Path("Election_Data")
    
    # Initialize the results structure with enhanced metadata
    results = {
        "metadata": {
            "state": "Texas",
            "source": "OpenElections",
            "years_covered": [],
            "focus": "Clean geographic political patterns",
            "processed_date": "2025-11-02",
            "categorization_system": {
                "competitiveness_scale": {
                    "Republican": [
                        {
                            "category": "Annihilation",
                            "range": "R+40%+",
                            "color": "#67000d"
                        },
                        {
                            "category": "Dominant",
                            "range": "R+30-40%",
                            "color": "#a50f15"
                        },
                        {
                            "category": "Stronghold",
                            "range": "R+20-30%",
                            "color": "#cb181d"
                        },
                        {
                            "category": "Safe",
                            "range": "R+10-20%",
                            "color": "#ef3b2c"
                        },
                        {
                            "category": "Likely",
                            "range": "R+5.5-10%",
                            "color": "#fb6a4a"
                        },
                        {
                            "category": "Lean",
                            "range": "R+1-5.5%",
                            "color": "#fcae91"
                        },
                        {
                            "category": "Tilt",
                            "range": "R+0.5-1%",
                            "color": "#fee8c8"
                        }
                    ],
                    "Tossup": [
                        {
                            "category": "Tossup",
                            "range": "±0.5%",
                            "color": "#f7f7f7"
                        }
                    ],
                    "Democratic": [
                        {
                            "category": "Tilt",
                            "range": "D+0.5-1%",
                            "color": "#e1f5fe"
                        },
                        {
                            "category": "Lean",
                            "range": "D+1-5.5%",
                            "color": "#c6dbef"
                        },
                        {
                            "category": "Likely",
                            "range": "D+5.5-10%",
                            "color": "#9ecae1"
                        },
                        {
                            "category": "Safe",
                            "range": "D+10-20%",
                            "color": "#6baed6"
                        },
                        {
                            "category": "Stronghold",
                            "range": "D+20-30%",
                            "color": "#3182bd"
                        },
                        {
                            "category": "Dominant",
                            "range": "D+30-40%",
                            "color": "#08519c"
                        },
                        {
                            "category": "Annihilation",
                            "range": "D+40%+",
                            "color": "#08306b"
                        }
                    ]
                },
                "office_types": [
                    "Federal",
                    "State",
                    "Judicial",
                    "Other"
                ],
                "enhanced_features": [
                    "Competitiveness categorization for each county",
                    "Contest type classification (Federal/State/Judicial)",
                    "Office ranking system for analysis prioritization",
                    "Color coding compatible with political geography visualization"
                ]
            }
        },
        "results_by_year": {}
    }
    
    # Define the CSV files to process (county-level data or precinct directories)
    csv_files = {
        2000: "20001107__tx__general__county.csv",
        2002: "20021105__tx__general__county.csv",
        2004: "20041102__tx__general__county.csv",
        2006: "20061107__tx__general__county.csv",
        2008: "20081104__tx__general__county.csv",
        2010: "20101102__tx__general__county.csv",
        2012: "20121106__tx__general__county.csv",
        2014: "2014/counties/20141104__tx__general__county.csv",
        2016: "20161108__tx__general__county.csv",
        2018: "20181106__tx__general__county.csv",
        2020: "20201103__tx__general__county_from_precinct.csv",  # Aggregated from precinct data
        2022: "20221108__tx__general__county_from_precinct.csv",  # Aggregated from precinct data
        2024: "2024/counties",   # Precinct-level data in directory
    }
    
    # Process each year
    for year, filename in sorted(csv_files.items()):
        filepath = election_dir / filename
        
        print(f"Processing {year}...")
        
        try:
            # Check if this is a directory (precinct data) or file
            if filepath.is_dir():
                # Aggregate precinct data from directory
                df = aggregate_precinct_to_county(filepath, year)
                if df is None:
                    print(f"Warning: Could not aggregate precinct data for {year}, skipping")
                    continue
            elif filepath.exists():
                # Check if it's a precinct file or county file
                if '__precinct' in str(filepath):
                    # Single precinct file - aggregate it
                    df = aggregate_single_precinct_file(filepath, year)
                    if df is None:
                        print(f"Warning: Could not aggregate precinct file for {year}, skipping")
                        continue
                else:
                    # Read county-level CSV directly
                    df = pd.read_csv(filepath)
            else:
                print(f"Warning: {filepath} not found, skipping year {year}")
                continue
            
            # Initialize year data
            if year not in results["results_by_year"]:
                results["results_by_year"][year] = {}
                results["metadata"]["years_covered"].append(year)
            
            # Process by office type
            offices = df['office'].unique()
            
            for office in offices:
                # Skip NaN or non-string office values
                if pd.isna(office) or not isinstance(office, str):
                    continue
                    
                office_data = df[df['office'] == office].copy()
                
                # Determine contest category
                if 'President' in office or 'VicePresident' in office:
                    category = "presidential"
                    contest_key = "president"
                elif 'U.S. Senate' in office or 'Senate' in office:
                    category = "us_senate"
                    contest_key = "us_senate"
                elif 'Lieutenant Governor' in office:
                    category = "statewide"
                    contest_key = "lt_governor"
                elif 'Governor' in office:
                    category = "statewide"
                    contest_key = "governor"
                elif 'Attorney General' in office:
                    category = "statewide"
                    contest_key = "attorney_general"
                elif 'Comptroller' in office:
                    category = "statewide"
                    contest_key = "comptroller"
                elif 'Agriculture Commissioner' in office or 'Commissioner of Agriculture' in office:
                    category = "statewide"
                    contest_key = "agriculture_commissioner"
                elif 'Railroad Commissioner' in office or 'Railroad Commission' in office:
                    category = "statewide"
                    contest_key = "railroad_commissioner"
                else:
                    # Skip other offices for now
                    continue
                
                # Initialize category if not exists
                if category not in results["results_by_year"][year]:
                    results["results_by_year"][year][category] = {}
                
                # Initialize contest
                if contest_key not in results["results_by_year"][year][category]:
                    results["results_by_year"][year][category][contest_key] = {
                        "contest_name": office,
                        "year": year,
                        "results": {},
                        "dem_candidate": None,
                        "rep_candidate": None,
                        "other_votes": 0,
                        "total_votes": 0
                    }
                
                contest = results["results_by_year"][year][category][contest_key]
                
                # Group by county and party
                for county_name in office_data['county'].unique():
                    county_data = office_data[office_data['county'] == county_name]
                    
                    norm_county = normalize_county_name(county_name)
                    
                    if norm_county not in contest["results"]:
                        contest["results"][norm_county] = {
                            "county": norm_county,
                            "contest": office,
                            "year": str(year),
                            "dem_votes": 0,
                            "rep_votes": 0,
                            "other_votes": 0,
                            "total_votes": 0,
                            "two_party_total": 0,
                            "dem_candidate": None,
                            "rep_candidate": None
                        }
                    
                    # Initialize party breakdown tracking
                    if "party_breakdown" not in contest["results"][norm_county]:
                        contest["results"][norm_county]["party_breakdown"] = {}
                    
                    # Sum votes by party
                    for _, row in county_data.iterrows():
                        party = str(row.get('party', '')).upper()
                        
                        # Handle votes - some rows have party in votes column
                        try:
                            votes = int(row.get('votes', 0))
                        except (ValueError, TypeError):
                            # Skip rows where votes can't be parsed
                            continue
                        
                        candidate = row.get('candidate', '')
                        
                        # Skip "Total" rows
                        if 'Total' in str(candidate):
                            continue
                        
                        if party == 'DEM':
                            contest["results"][norm_county]["dem_votes"] += votes
                            if not contest["results"][norm_county]["dem_candidate"] and candidate:
                                contest["results"][norm_county]["dem_candidate"] = candidate
                                if not contest["dem_candidate"]:
                                    contest["dem_candidate"] = candidate
                        elif party == 'REP':
                            contest["results"][norm_county]["rep_votes"] += votes
                            if not contest["results"][norm_county]["rep_candidate"] and candidate:
                                contest["results"][norm_county]["rep_candidate"] = candidate
                                if not contest["rep_candidate"]:
                                    contest["rep_candidate"] = candidate
                        else:
                            contest["results"][norm_county]["other_votes"] += votes
                        
                        # Track ALL parties for detailed breakdown
                        # For 2006 Governor specifically, break out IND candidates by name (Kinky Friedman & Carole Keeton Strayhorn)
                        # For other contests, just track by party (LIB, GRN, etc.)
                        if party and party not in ['DEM', 'REP', '', 'NAN']:
                            # Special handling for 2006 Governor: break out individual IND/WI candidates
                            if year == 2006 and office.lower() == 'governor' and party in ['IND', 'WI'] and candidate and str(candidate).strip():
                                # Clean up candidate name for key
                                clean_candidate = str(candidate).strip().replace(' ', '_').replace('"', '').replace("'", '').replace('.', '')
                                party_key = f"{party}_{clean_candidate}"
                            else:
                                # For all other contests, just use the party abbreviation
                                party_key = party
                            
                            if party_key not in contest["results"][norm_county]["party_breakdown"]:
                                contest["results"][norm_county]["party_breakdown"][party_key] = 0
                            contest["results"][norm_county]["party_breakdown"][party_key] += votes
                    
                    # Calculate county totals
                    county_result = contest["results"][norm_county]
                    county_result["total_votes"] = (
                        county_result["dem_votes"] + 
                        county_result["rep_votes"] + 
                        county_result["other_votes"]
                    )
                    county_result["two_party_total"] = (
                        county_result["dem_votes"] + 
                        county_result["rep_votes"]
                    )
                    
                    # Calculate competitiveness
                    if county_result["total_votes"] > 0:
                        dem_pct = (county_result["dem_votes"] / county_result["total_votes"]) * 100
                        rep_pct = (county_result["rep_votes"] / county_result["total_votes"]) * 100
                        margin_pct = abs(dem_pct - rep_pct)
                        winner = 'Democratic' if dem_pct > rep_pct else 'Republican'
                        
                        # Determine category
                        if margin_pct >= 40:
                            category_name = "Annihilation"
                        elif margin_pct >= 30:
                            category_name = "Dominant"
                        elif margin_pct >= 20:
                            category_name = "Stronghold"
                        elif margin_pct >= 10:
                            category_name = "Safe"
                        elif margin_pct >= 5.5:
                            category_name = "Likely"
                        elif margin_pct >= 1:
                            category_name = "Lean"
                        elif margin_pct >= 0.5:
                            category_name = "Tilt"
                        else:
                            category_name = "Tossup"
                            winner = "Tossup"
                        
                        # Get color for this competitiveness level
                        color = get_competitiveness_color(category_name, winner)
                        
                        # Create code (e.g., "R_LIKELY", "D_SAFE", "TOSSUP")
                        if winner == "Tossup":
                            code = "TOSSUP"
                        else:
                            party_code = "R" if winner == "Republican" else "D"
                            code = f"{party_code}_{category_name.upper()}"
                        
                        county_result["competitiveness"] = {
                            "category": category_name,
                            "party": winner,
                            "code": code,
                            "color": color,
                            "description": f"{category_name} {winner}" if winner != "Tossup" else "Tossup"
                        }
                        
                        # Add margin information
                        county_result["margin"] = county_result["dem_votes"] - county_result["rep_votes"]
                        county_result["margin_pct"] = round(margin_pct, 2)
                        county_result["winner"] = "DEM" if dem_pct > rep_pct else ("REP" if rep_pct > dem_pct else "TIE")
                        
                        # Add all party breakdown
                        all_parties = {
                            "DEM": county_result["dem_votes"],
                            "REP": county_result["rep_votes"]
                        }
                        
                        # Add ALL tracked third parties (not just LIB, GRN, IND)
                        # This will now include parties like WI (Write-in), IND for independents, etc.
                        if "party_breakdown" in county_result:
                            for party, votes in county_result["party_breakdown"].items():
                                all_parties[party] = votes
                        
                        # Verify totals match (sanity check)
                        tracked_total = sum(all_parties.values())
                        if abs(county_result["total_votes"] - tracked_total) > 1:  # Allow 1 vote rounding difference
                            # If there's a mismatch, add an OTHER category for unaccounted votes
                            all_parties["OTHER"] = county_result["total_votes"] - tracked_total
                        
                        county_result["all_parties"] = all_parties
                        
                        # Clean up temporary party_breakdown
                        # NOTE: Commented out to preserve party_breakdown for debugging
                        # if "party_breakdown" in county_result:
                        #     del county_result["party_breakdown"]
                
                # Calculate statewide totals
                for county_result in contest["results"].values():
                    contest["total_votes"] += county_result["total_votes"]
                    contest["other_votes"] += county_result["other_votes"]
        
        except Exception as e:
            print(f"Error processing {year}: {e}")
            import traceback
            traceback.print_exc()
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Save to JSON file
    output_file = data_dir / "texas_election_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nSuccessfully created {output_file}")
    print(f"   Years covered: {sorted(results['metadata']['years_covered'])}")
    print(f"   Total contests: {sum(len(year_data) for year_data in results['results_by_year'].values())}")
    
    return results

if __name__ == "__main__":
    print("Texas Election Data Processor")
    print("=" * 50)
    results = process_texas_election_data()
    print("\n✅ Processing complete!")
