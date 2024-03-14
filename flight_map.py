import folium
import math
import numpy as np
import data_cleaning
import pyproj

# Subesetting ICAO, LON, LAT from dataframe
airport_df = data_cleaning.airportclean[['ICAO', 'Longitude', 'Latitude']]

def draw_flight_path(start_ICAO, end_ICAO):

    # Retrieve Lat and Long from dataframe
    startLong = airport_df.loc[airport_df['ICAO'] == start_ICAO, 'Latitude'].iloc[0]
    startLat = airport_df.loc[airport_df['ICAO'] == start_ICAO, 'Longitude'].iloc[0]
    endLong = airport_df.loc[airport_df['ICAO'] == end_ICAO, 'Latitude'].iloc[0]
    endLat = airport_df.loc[airport_df['ICAO'] == end_ICAO, 'Longitude'].iloc[0]

    # Calculate distance between points
    g = pyproj.Geod(ellps='WGS84')
    (az12, az21, dist) = g.inv(startLong, startLat, endLong, endLat)

    # calculate line string along path with segments <= 1 km
    lonlats = g.npts(startLong, startLat, endLong, endLat, 1 + int(dist / 1000), initial_idx=0, terminus_idx=0)
    
    # Draw Polyline to map
    folium.PolyLine(
        locations=lonlats,
        color='red',
        tooltip=start_ICAO + '->' + end_ICAO,
        weight=2
    ).add_to(m)

# Draw Folium Map
m = folium.Map(location=(0,0), tiles="cartodb positron", zoom_start=1.5)

#draw_flight_path()

# Save map temporarily
m.save('map_test.html')




