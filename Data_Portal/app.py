# Tutorial Imports 
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Graphing/plotting/ spatial imports 
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import Point
import matplotlib as mpl
from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.patches as Patches

app = Dash() 

localdatapath = "/Users/griffinberonio/Documents/Holloway_Group/Data/WashU_V6_NA/Dane_CO_V6NA01.CNNPM25_2021-2023_grids.gpkg"

gdf = gpd.read_file(localdatapath)

counties = gpd.read_file("/Users/griffinberonio/Documents/Holloway_Group/Data/map_shapefiles/tl_2023_us_county/tl_2023_us_county.shp")
counties = counties.to_crs(epsg=4326)
danecounty = counties[counties['GEOID'] == '55025']

daneplot = gdf.plot()

hotspots = gdf[gdf['PM25'] > 8].copy()




if __name__ == '__main__':

    app.run(debug=True)