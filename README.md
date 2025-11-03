# Texas Election Realignment Map

An interactive visualization of Texas election results from 2000-2024, showcasing voting patterns and political realignment across all 254 Texas counties.

## Features

- **13 Years of Data**: 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024
- **33 Contests**: Presidential, Senate, and statewide offices
- **15-Level Competitiveness Scale**: From "Solid Democratic" to "Solid Republican"
- **Interactive Mapbox GL Visualization**: County-level detail with hover tooltips

## Special Features

### 2006 Governor Race
The 2006 Texas gubernatorial election was a historic four-way contest featuring:
- **Rick Perry (R)** - Incumbent Governor
- **Chris Bell (D)** - Democratic nominee
- **Carole Keeton Strayhorn (I)** - Texas Comptroller running as independent
- **Kinky Friedman (I)** - Musician and author

This race is uniquely handled in the visualization with individual breakdowns for independent candidates Strayhorn and Friedman, rather than aggregating them as "OTHER" like other contests.

## Technical Stack

- **Mapbox GL JS v3.0.1** - Interactive mapping
- **Python 3.13** - Data processing with pandas/GeoPandas
- **GeoJSON** - Texas county boundaries from TIGER/Line shapefiles
- **OpenElections Data** - CSV data sources for election results

## Data Sources

- County boundaries: U.S. Census Bureau TIGER/Line Shapefiles (2020)
- Election results: OpenElections Project (https://github.com/openelections)

## Files

- `index.html` - Main map interface
- `data/texas_election_results.json` - Processed election results
- `TX_Data/tl_2020_48_county20.geojson` - County boundary data
- `process_tx_election_data.py` - Data processing script

## Usage

Simply open `index.html` in a web browser, or view the live deployment at:
https://tenjin25.github.io/TXRealignment/

## License

Data sourced from OpenElections Project. Map visualization code adapted from NC Election analysis project.
