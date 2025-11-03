# Texas Election Realignment Map

An interactive visualization of Texas election results from 2000-2024, showcasing voting patterns and political realignment across all 254 Texas counties.

## Features

- **13 Years of Data**: 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024
- **28 Contests**: Presidential, Senate, and statewide offices
- **Complete Coverage**: 
  - 2024: President, U.S. Senate, Railroad Commissioner (all 254 counties)
  - 2022: Governor, Lieutenant Governor, Attorney General, Comptroller, Land Commissioner, Agriculture Commissioner, Railroad Commissioner
  - 2020: President, U.S. Senate, Railroad Commissioner
  - Historical races back to 2000
- **Normalized Data**: Consistent contest names and full candidate names across all years
- **18 Multi-word County Names**: Properly formatted (La Salle, De Witt, El Paso, etc.)
- **15-Level Competitiveness Scale**: From "Annilation Democratic" to "Annihilation Republican"
- **Interactive Mapbox GL Visualization**: County-level detail with hover tooltips

## Political Trends & Analysis

### Presidential Race Evolution (2000-2024)

Texas has maintained its Republican lean in presidential elections, but with significant internal shifts:

**Statewide Margins:**
- **2000**: Bush (R+21.91%) - 3,799,639 vs Gore 2,433,746
- **2008**: McCain (R+11.87%) - Lowest Republican margin until 2020
- **2020**: Trump (R+5.66%) - Closest race since 1996
- **2024**: Trump (R+13.88%) - Republican rebound

**24-Year Net Shift**: Despite Trump's 2024 improvement, the state has shifted 8.03 points more Republican since 2000, driven largely by dramatic realignment in South Texas and rural areas offsetting urban Democratic gains.

### The Great South Texas Realignment

The most dramatic political shift in Texas has occurred along the Rio Grande Valley border:

**Starr County** (Most Dramatic Swing):
- 2000: D+54.6% → 2024: **R+16.1%** (70.6-point swing)
- 2012: Peak at D+73.8%
- Historic flip from one of Texas's bluest counties to Republican

**Other Major Border Flips:**
- **Zapata County**: D+26.4% (2000) → R+22.6% (2024) - 49-point swing
- **Maverick County**: D+31.2% (2000) → R+18.6% (2024) - 50-point swing
- **Hidalgo County** (McAllen): D+23.2% (2000) → R+2.9% (2024) - First Republican presidential win
- **Cameron County** (Brownsville): D+8.9% (2000) → R+5.8% (2024)
- **Webb County** (Laredo): D+16.2% (2000) → R+2.1% (2024)

### Metropolitan Countercurrent

While rural and border counties trended Republican, major metros shifted Democratic:

**Urban Blue Shift:**
- **Travis County** (Austin): R+5.9% (2000) → **D+40.1%** (2024) - 46-point Democratic swing
- **Dallas County**: R+7.9% (2000) → **D+22.6%** (2024) - 30-point swing
- **Harris County** (Houston): R+3.5% (2000) → **D+5.6%** (2024)

**Suburban Transformation:**
- **Collin County** (Plano/Frisco): R+49.9% (2000) → R+11.4% (2024) - 38-point Democratic swing
- **Denton County**: R+43.6% (2000) → R+13.4% (2024) - 30-point Democratic swing
- **Williamson County**: R+42.0% (2000) → R+2.5% (2024) - 39-point swing, now highly competitive
- **Fort Bend County**: R+21.5% (2000) → **D+1.6%** (2024) - Flipped Democratic
- **Tarrant County** (Fort Worth): R+24.6% (2000) → R+5.2% (2024) - Now a swing county

### 2024 Battleground Counties

The most competitive counties in the 2024 presidential race (under 6% margin):

1. **Fort Bend County** (Houston suburbs): D+1.6% - 352,902 votes
2. **Webb County** (Laredo): R+2.1% - 65,393 votes
3. **Williamson County** (Austin suburbs): R+2.5% - 303,076 votes
4. **Hidalgo County** (McAllen): R+2.9% - 215,277 votes
5. **Tarrant County** (Fort Worth): R+5.2% - 811,127 votes
6. **Harris County** (Houston): D+5.6% - 1,531,466 votes
7. **Hays County** (San Marcos): D+5.7% - 123,966 votes
8. **Cameron County** (Brownsville): R+5.8% - 115,249 votes

### Major Metropolitan Results (2024)

**Solidly Democratic:**
- **Travis County** (Austin): D+40.1% - 569,749 votes
- **Dallas County**: D+22.6% - 833,495 votes
- **El Paso County**: D+15.3% - 248,280 votes
- **Bexar County** (San Antonio): D+9.9% - 748,934 votes

**Competitive/Republican:**
- **Harris County** (Houston): D+5.6% - 1,531,466 votes (largest county, highly competitive)
- **Tarrant County** (Fort Worth): R+5.2% - 811,127 votes
- **Collin County** (Plano): R+11.5% - 501,649 votes
- **Denton County**: R+13.4% - 442,024 votes

## Special Features

### 2006 Governor Race
The 2006 Texas gubernatorial election was a historic four-way contest featuring:
- **Rick Perry (R)** - Incumbent Governor
- **Chris Bell (D)** - Democratic nominee
- **Carole Keeton Strayhorn (I)** - Texas Comptroller running as independent
- **Kinky Friedman (I)** - Musician and author

This race is uniquely handled in the visualization with individual breakdowns for independent candidates Strayhorn and Friedman, rather than aggregating them as "OTHER" like other contests.

## Data Quality & Normalization

### County Name Handling
The project properly handles 18 multi-word Texas county names that require space formatting:
- La Salle, De Witt, Deaf Smith, El Paso, Fort Bend, Jeff Davis, Jim Hogg, Jim Wells, Live Oak, Palo Pinto, Red River, San Augustine, San Jacinto, San Patricio, San Saba, Tom Green, Val Verde, Van Zandt

### Contest Name Standardization
All contest names are normalized for consistency:
- "U.S Sen" → "U.S. Senate"
- "RR Comm 1" → "Railroad Commissioner"
- "Ag Comm" → "Agriculture Commissioner"
- "Land Comm" → "Land Commissioner"

### Candidate Names
Full candidate names are provided for all major party candidates, including:
- **2024**: Kamala Harris, Donald Trump, Colin Allred, Ted Cruz, Katherine Culbert, Christi Craddick
- **2022**: Dawn Buckingham, Jay Kleberg, Sid Miller, Susan Hays, Wayne Christian, Luke Warford
- And all historical candidates back to 2000

## Technical Stack

- **Mapbox GL JS v3.0.1** - Interactive mapping
- **Python 3.13** - Data processing with pandas
- **GeoJSON** - Texas county boundaries from TIGER/Line shapefiles
- **OpenElections Data** - CSV data sources for election results

## Data Sources

- **County boundaries**: U.S. Census Bureau TIGER/Line Shapefiles (2020) - 254 Texas counties
- **Election results 2000-2018**: OpenElections Project (https://github.com/openelections)
- **Election results 2020**: VTD-aligned precinct-level data, aggregated to county level
- **Election results 2022**: Texas Legislative Council VTD-aligned data (`2022_General_Election_Returns-aligned.csv`)
  - Supplemented with statewide races (Land Commissioner, Agriculture Commissioner, Railroad Commissioner)
- **Election results 2024**: Texas Legislative Council. (2024). *Comprehensive Election Datasets - Compressed Format: 2024 General Election Returns*. Texas Open Data Portal. Retrieved from https://data.capitol.texas.gov/dataset/comprehensive-election-datasets-compressed-format/resource/e1cd6332-6a7a-4c78-ad2a-852268f6c7a2
  - VTD-aligned CSV format (`2024_General_Election_Returns-Aligned.csv`)

## Files

### Core Application
- `index.html` - Main map interface with Mapbox GL visualization
- `data/texas_election_results.json` - Processed election results (28 contests across 13 years)
- `TX_Data/tl_2020_48_county20.geojson` - County boundary data (254 Texas counties)

### Data Processing
- `process_tx_election_data.py` - Main data processing script with:
  - County name normalization (handles 18 multi-word counties)
  - Contest name normalization (standardizes office names)
  - Candidate name resolution (full names for all major candidates)
  - Supplemental data integration for 2022 statewide races

### Verification Scripts
- `verify_all.py` - Comprehensive data quality verification
- `check_2022.py` - Verify 2022 contest normalization
- `check_2024_contests.py` - Verify 2024 contest normalization
- `check_rr_2024.py` - Verify 2024 Railroad Commissioner candidate names

## Usage

Simply open `index.html` in a web browser, or view the live deployment at:
https://tenjin25.github.io/TXRealignment/

## License

Data sourced from OpenElections Project. Map visualization code adapted from NC Election analysis project.
