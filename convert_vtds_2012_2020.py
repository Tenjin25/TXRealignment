import geopandas as gpd
import os

# Paths to your shapefiles
shp_2012 = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TXRealignments\TXdata\tl_2012_48_vtd10\tl_2012_48_vtd10.shp"
shp_2020 = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TXRealignments\TXdata\tl_2020_48_vtd20\tl_2020_48_vtd20.shp"

# Output paths
geojson_2012 = os.path.splitext(shp_2012)[0] + ".geojson"
geojson_2020 = os.path.splitext(shp_2020)[0] + ".geojson"

# Convert 2012
print(f"Converting 2012 VTD shapefile: {shp_2012}")
gdf_2012 = gpd.read_file(shp_2012)
gdf_2012.to_file(geojson_2012, driver="GeoJSON")
print(f"2012 VTDs saved to {geojson_2012}")

# Convert 2020
print(f"Converting 2020 VTD shapefile: {shp_2020}")
gdf_2020 = gpd.read_file(shp_2020)
gdf_2020.to_file(geojson_2020, driver="GeoJSON")
print(f"2020 VTDs saved to {geojson_2020}")
