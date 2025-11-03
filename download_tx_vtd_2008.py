
# Requirements: geopandas, shapely, requests, beautifulsoup4
# Install with: pip install geopandas shapely requests beautifulsoup4

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import zipfile
import geopandas as gpd

BASE_URL = "https://www2.census.gov/geo/tiger/TIGER2008/48_TEXAS/"
DOWNLOAD_DIR = "TX_VTD_2008"
GEOJSON_DIR = "TX_VTD_2008_GEOJSON"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(GEOJSON_DIR, exist_ok=True)

# Get the list of all county folders in the directory
s = requests.Session()
s.verify = False  # Disable SSL verification
response = s.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")
county_dirs = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('48') and a['href'].endswith('_County/')]

print(f"Found {len(county_dirs)} county directories.")

for county_dir in county_dirs:
    county_url = BASE_URL + county_dir
    county_name = county_dir.strip('/').split('_', 1)[-1]
    # Get the VTD zip file in the county directory
    resp = s.get(county_url)
    soup2 = BeautifulSoup(resp.text, "html.parser")
    vtd_zip_links = [a['href'] for a in soup2.find_all('a', href=True) if 'vtd' in a['href'].lower() and a['href'].endswith('.zip')]
    for zip_link in vtd_zip_links:
        file_url = county_url + zip_link
        local_zip_path = os.path.join(DOWNLOAD_DIR, zip_link)
        print(f"Downloading {file_url} ...")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                r = s.get(file_url, stream=True)
                with open(local_zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Saved to {local_zip_path}")
                break
            except Exception as e:
                print(f"Download failed (attempt {attempt+1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    print(f"Skipping {file_url} after {max_retries} failed attempts.")
                    continue
        # Check if file is a valid ZIP before unzipping
        is_zip = False
        try:
            with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
                is_zip = True
        except zipfile.BadZipFile:
            print(f"Warning: {local_zip_path} is not a valid ZIP file. Skipping.")
        if not is_zip:
            continue
        # Unzip
        with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
            extract_dir = os.path.join(DOWNLOAD_DIR, zip_link.replace('.zip', ''))
            os.makedirs(extract_dir, exist_ok=True)
            zip_ref.extractall(extract_dir)
        # Find the shapefile
        shp_files = [f for f in os.listdir(extract_dir) if f.endswith('.shp')]
        if not shp_files:
            print(f"No shapefile found in {extract_dir}")
            continue
        shp_path = os.path.join(extract_dir, shp_files[0])
        # Convert to GeoJSON
        try:
            gdf = gpd.read_file(shp_path)
            geojson_path = os.path.join(GEOJSON_DIR, zip_link.replace('.zip', '.geojson'))
            gdf.to_file(geojson_path, driver='GeoJSON')
            print(f"GeoJSON saved: {geojson_path}")
        except Exception as e:
            print(f"Error converting {shp_path} to GeoJSON: {e}")


# Merge all county GeoJSONs into one statewide GeoJSON
import glob
all_geojson_files = glob.glob(os.path.join(GEOJSON_DIR, '*.geojson'))
print(f"Merging {len(all_geojson_files)} county GeoJSONs into one statewide GeoJSON...")
gdfs = []
for gj in all_geojson_files:
    try:
        gdf = gpd.read_file(gj)
        gdfs.append(gdf)
    except Exception as e:
        print(f"Error reading {gj}: {e}")
if gdfs:
    statewide_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=gdfs[0].crs)
    statewide_geojson_path = os.path.join(GEOJSON_DIR, 'TX_VTD_2008_statewide.geojson')
    statewide_gdf.to_file(statewide_geojson_path, driver='GeoJSON')
    print(f"Statewide GeoJSON saved: {statewide_geojson_path}")
else:
    print("No county GeoJSONs found to merge.")
print("All VTD shapefiles downloaded, converted, and merged into statewide GeoJSON.")
