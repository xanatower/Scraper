import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from shapely.geometry import Point

# Step 1: Geocode your addresses to get coordinates
def geocode_addresses(addresses):
    geolocator = Nominatim(user_agent="sa1_mapping")
    results = []
    
    for address in addresses:
        try:
            location = geolocator.geocode(address + ", Melbourne, Australia")
            if location:
                results.append({
                    'address': address,
                    'latitude': location.latitude,
                    'longitude': location.longitude
                })
            else:
                results.append({'address': address, 'latitude': None, 'longitude': None})
        except Exception as e:
            print(f"Error geocoding {address}: {e}")
            results.append({'address': address, 'latitude': None, 'longitude': None})
    
    return pd.DataFrame(results)

# Step 2: Convert addresses to GeoDataFrame
def addresses_to_geodf(addresses_df):
    # Filter out any addresses that couldn't be geocoded
    valid_locations = addresses_df.dropna(subset=['latitude', 'longitude'])
    
    # Create geometry column
    geometry = [Point(xy) for xy in zip(valid_locations['longitude'], valid_locations['latitude'])]
    
    # Create GeoDataFrame
    geo_df = gpd.GeoDataFrame(valid_locations, geometry=geometry, crs="EPSG:4326")
    return geo_df

# Step 3: Spatial join with SA1 boundaries to get SA1 codes
def match_addresses_to_sa1(addresses_geo_df, sa1_boundaries_path):
    # Load SA1 boundaries (you'll need to download this from ABS)
    sa1_boundaries = gpd.read_file(sa1_boundaries_path)
    
    # Make sure CRS matches
    if sa1_boundaries.crs != addresses_geo_df.crs:
        sa1_boundaries = sa1_boundaries.to_crs(addresses_geo_df.crs)
    
    # Perform spatial join
    joined = gpd.sjoin(addresses_geo_df, sa1_boundaries, how="left", predicate="within")
    
    # Return addresses with SA1 codes
    return joined[['address', 'latitude', 'longitude', 'SA1_CODE21']]  # Adjust 'SA1_CODE' to match your shapefile column name

def check_geo_social_addresses(list_of_address):
    # Path to SA1 boundaries shapefile (you need to download this from ABS)
    sa1_boundaries_path = "SA1_2021_AUST_GDA2020.shp"
   
    # Process addresses
    geocoded_addresses = geocode_addresses(list_of_address)
    addresses_geo = addresses_to_geodf(geocoded_addresses)
    addresses_with_sa1 = match_addresses_to_sa1(addresses_geo, sa1_boundaries_path)

    return addresses_with_sa1



def adhoc_run_geo_social(list_of_address):
    '''
    ADHoc Run of geosocial address
    '''
    input_geo_social_profile_df = pd.read_csv("H:\\My Drive\\House_Hunting\\Scraper\\assets\\Northern_Social.csv")
    geo_social_profile_df = input_geo_social_profile_df[["SA1", "Percent (%)"]]

    
    output_geo_df = check_geo_social_addresses(list_of_address)
    address_df = pd.DataFrame({'Address_clean':list_of_address})

    merged_df = address_df.merge(
        output_geo_df,
        left_on='Address_clean',  # Column name in output_df
        right_on='address',       # Column name in addresses_with_sa1
        how='left'                # Keep all rows from output_df
    )

    merged_df = merged_df.drop(columns=['address'])

    # merged_df.rename({"SA1_CODE21":"SA1"}, inplace=True, axis=1)

    merge_df_with_percentage = merged_df.merge(
        geo_social_profile_df,
        left_on='SA1_CODE21',  # Column name in output_df
        right_on='SA1',       # Column name in addresses_with_sa1
        how='left'                # Keep all rows from output_df
    )


    merge_df_with_percentage = merge_df_with_percentage.drop(columns=['SA1'])    


    print(merge_df_with_percentage)