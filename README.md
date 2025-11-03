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
