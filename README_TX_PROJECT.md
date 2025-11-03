# Texas Political Realignment Project

## Project Overview
Interactive visualization of Texas political trends from 2000-2024, showing county-level voting patterns and realignment analysis.

## Files Created

### 1. **TXMap.html**
- Main interactive map for Texas
- Retrofitted from NCMap.html
- Uses Mapbox GL JS for rendering
- Features:
  - County-level election results
  - Interactive sidebar with detailed analysis
  - Contest selector dropdown
  - Legend with competitiveness categories
  - Responsive design

### 2. **index_new.html**
- Landing page for the project
- Links to both Texas and North Carolina maps
- Clean, modern design with gradient background
- Feature list and project information

### 3. **data/texas_election_results.json**
- Comprehensive election data for Texas (2000-2018)
- Enhanced metadata structure including:
  - Competitiveness categorization system
  - Color coding for visualization
  - Office type classifications
  - All party vote breakdowns

### 4. **process_tx_election_data.py**
- Python script to process OpenElections CSV data
- Creates structured JSON for the map
- Features:
  - Handles multiple election years
  - Calculates competitiveness categories
  - Assigns colors based on margins
  - Includes candidate names and vote totals

### 5. **TX_Data/tl_2020_48_county20/tl_2020_48_county20.geojson**
- Texas county boundaries (converted from shapefile)
- Used for map visualization

## Data Structure

### Competitiveness Categories
The system uses a 15-level competitiveness scale:

**Republican:**
- Annihilation (R+40%+) - #67000d
- Dominant (R+30-40%) - #a50f15
- Stronghold (R+20-30%) - #cb181d
- Safe (R+10-20%) - #ef3b2c
- Likely (R+5.5-10%) - #fb6a4a
- Lean (R+1-5.5%) - #fcae91
- Tilt (R+0.5-1%) - #fee8c8

**Tossup:**
- Tossup (±0.5%) - #f7f7f7

**Democratic:**
- Tilt (D+0.5-1%) - #e1f5fe
- Lean (D+1-5.5%) - #c6dbef
- Likely (D+5.5-10%) - #9ecae1
- Safe (D+10-20%) - #6baed6
- Stronghold (D+20-30%) - #3182bd
- Dominant (D+30-40%) - #08519c
- Annihilation (D+40%+) - #08306b

## Election Data Coverage

### Years Included:
- 2000, 2004, 2006, 2008, 2010, 2012, 2016, 2018

### Offices Covered:
- **Federal:** President, U.S. Senate
- **State:** Governor, Lieutenant Governor, Attorney General, Comptroller, Agriculture Commissioner, Railroad Commissioner

### County Coverage:
All 254 Texas counties

## Data Sources
- **Election Data:** OpenElections (openelections.net)
- **Geographic Data:** U.S. Census Bureau TIGER/Line Shapefiles
- **Conversion:** GeoPandas/Fiona

## Technical Stack
- **Frontend:** HTML5, CSS3, JavaScript
- **Mapping:** Mapbox GL JS v3.0.1
- **Data Processing:** Python, Pandas
- **Utilities:** Turf.js, PapaParse

## Next Steps

### To Complete the Project:

1. **Add More Years:**
   - Process 2014, 2020, 2022, 2024 data
   - Update CSV file paths in processor script

2. **Enhance Features:**
   - Add search functionality for counties
   - Implement historical trend analysis
   - Add demographic overlays
   - Create downloadable reports

3. **Data Improvements:**
   - Add precinct-level data where available
   - Include voter registration statistics
   - Add demographic data from Census

4. **Testing:**
   - Test on mobile devices
   - Verify all county names match between GeoJSON and election data
   - Check for data gaps or anomalies

## File Locations
```
TXRealignments/
├── TXMap.html (main map)
├── index_new.html (landing page)
├── NCMap.html (comparison map)
├── process_tx_election_data.py (data processor)
├── convert_shp_to_geojson.py (shapefile converter)
├── data/
│   └── texas_election_results.json (election data)
├── TX_Data/
│   └── tl_2020_48_county20/
│       └── tl_2020_48_county20.geojson (county boundaries)
└── Election_Data/
    └── [multiple CSV files from OpenElections]
```

## Usage

1. **View the Map:**
   - Open `index_new.html` in a browser
   - Click "Explore Texas Map"

2. **Interact:**
   - Click counties to see detailed results
   - Use dropdown to select different contests
   - Toggle legend and controls as needed

3. **Process New Data:**
   ```bash
   python process_tx_election_data.py
   ```

## Author
Shamar Davis

## Date
November 2, 2025
