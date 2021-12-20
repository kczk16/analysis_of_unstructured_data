from geotext import GeoText
from collections import Counter

with open('around.txt') as f:
    ksionzka = f.readlines()

k = ksionzka[:500]
ksionzka = ' '.join(ksionzka)
ksionzka = ksionzka.replace('Bombay', 'Mumbai')
ksionzka = ksionzka.replace('Calcutta', 'Kolkata')

places = GeoText(ksionzka)
# print(places.cities)
Counter(places.cities)



import wikipedia
ny = wikipedia.page("Independent_city")
wiki_txt = ny.content
places = GeoText(wiki_txt)
places.countries


from geotext import GeoText
places = GeoText("Salt is a great city")
places.cities

import geonamescache
gc = geonamescache.GeonamesCache()
countries = gc.search_cities('Salt Lake City')


cities = list(set(places.cities))[:20]

import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="AroundTheWorld")
positions = dict()
for c in cities:
    while True:
        try:
            position = geolocator.geocode(c)
        except:
            time.sleep(5)
            continue
        break
    if position:
        location = [position.latitude, position.longitude]
        positions.update({c: location})
        del position
    else:
        print("Could not get position for {}".format(c))

print(positions)

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


df = pd.DataFrame.from_dict(positions, orient='index')
df = df.rename({0: 'Latitude', 1: 'Longitude'}, axis=1)
df = df.reset_index()

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

import plotly.express as px
px.line_geo(loc)
geo_df = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

# px.set_mapbox_access_token(open(".mapbox_token").read())
fig = px.scatter_mapbox(gdf, lat=gdf.geometry.y, lon=gdf.geometry.x, hover_name="index", zoom=3)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
fig, ax = plt.subplots(figsize=(15,10))
world.plot(ax=ax, alpha=0.4, color='grey')
gdf.plot(column='index', ax=ax, legend=True)
plt.title('Volcanoes')


import folium

loc = list(positions.values())
m = folium.Map(location=loc, tiles="OpenStreetMap", zoom_start=2)





geo_df = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))


gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

# px.set_mapbox_access_token(open(".mapbox_token").read())
# fig = px.scatter_mapbox(gdf, lat=gdf.geometry.y, lon=gdf.geometry.x, hover_name="index", zoom=3)
fig = px.line_geo(gdf, lat=gdf.geometry.y, lon=gdf.geometry.x, hover_name='index')
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


fig = px.scatter_mapbox(gdf, lat=gdf.geometry.y, lon=gdf.geometry.x, hover_name="index", zoom=3)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()