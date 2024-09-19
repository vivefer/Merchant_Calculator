import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load map of Nepal (Shapefile or GeoJSON)
nepal_map = gpd.read_file("local_unit.shp")

# Generate sample merchant data with latitude, longitude, and product usage/profit status
np.random.seed(42)
num_merchants = 1000
data = {
    'latitude': np.random.uniform(26, 30, num_merchants),  # Approx latitudes for Nepal
    'longitude': np.random.uniform(80, 88, num_merchants),  # Approx longitudes for Nepal
    'status': np.random.choice(['Profit', 'Loss', 'Not using'], num_merchants, 
                               p=[0.7, 0.2, 0.1])  # Majority in 'Profit'
}

# Convert to DataFrame
merchants_df = pd.DataFrame(data)

# Create a GeoDataFrame
geometry = gpd.points_from_xy(merchants_df['longitude'], merchants_df['latitude'])
geo_merchants = gpd.GeoDataFrame(merchants_df, geometry=geometry)

# Plot map of Nepal and overlay merchants
fig, ax = plt.subplots(figsize=(10, 10))
nepal_map.plot(ax=ax, color='lightgray')

# Plot merchants with different colors based on status
colors = {'Profit': 'green', 'Loss': 'red', 'Not using': 'gray'}
for status, color in colors.items():
    geo_merchants[geo_merchants['status'] == status].plot(ax=ax, marker='o', color=color, 
                                                          label=status, markersize=10)

plt.title("Merchants in Nepal and Their Product Usage Status")
plt.legend()
plt.show()
