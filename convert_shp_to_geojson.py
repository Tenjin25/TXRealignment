import geopandas as gpd
import os

# Input and output paths
shp_path = os.path.join('TX_Data', 'tl_2020_48_county20', 'tl_2020_48_county20.shp')
geojson_path = os.path.join('TX_Data', 'tl_2020_48_county20', 'tl_2020_48_county20.geojson')

def convert_shp_to_geojson(shp_path, geojson_path):
    gdf = gpd.read_file(shp_path)
    gdf.to_file(geojson_path, driver='GeoJSON')
    print(f"Converted {shp_path} to {geojson_path}")

if __name__ == "__main__":
    convert_shp_to_geojson(shp_path, geojson_path)
