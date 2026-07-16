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
import matplotlib.patches as mpatches

app = Dash() 

localdatapath = "/Users/griffinberonio/Documents/Holloway_Group/Data/WashU_V6_NA/Dane_CO_V6NA01.CNNPM25_2021-2023_grids.gpkg"

gdf = gpd.read_file(localdatapath)

counties = gpd.read_file("/Users/griffinberonio/Documents/Holloway_Group/Data/map_shapefiles/tl_2023_us_county/tl_2023_us_county.shp")
counties = counties.to_crs(epsg=4326)
danecounty = counties[counties['GEOID'] == '55025']



hotspots = gdf[gdf['PM25'] > 8].copy()

griddata = gdf.copy()
hotplot = hotspots.copy()
countyplot = danecounty.copy()

countyoutline = countyplot.dissolve(by='COUNTYFP')

fig, ax = plt.subplots(figsize = (10,8))

gdf.plot(column='PM25', ax=ax, legend=True, cmap='OrRd', edgecolor='k')
# countyoutline.plot(ax=ax, facecolor = False, color = 'black', linewidth=0.2)
countyoutline.boundary.plot(ax=ax, color='black', linewidth=3)
hotplot.plot(ax=ax, cmap="Purples", markersize=5, alpha=0.7, zorder=5)

legend_elements = [
    mpatches.Patch(color='red', alpha=0.7, label='PM₂.₅ Hotspots (Top Percentile)'),
    mpatches.Patch(color='#7C4DFF', alpha = 0.7, label = 'Concentration Above 8.0 µg/m³')]

ax.set_title('Dane County PM 2.5 Hotspots', fontsize = 18)
ax.legend(handles=legend_elements, loc='lower left', fontsize=18, framealpha=0.8)
ax.set_axis_off()

plt.tight_layout()


#Example bar graph:

gdf['Average'] = gdf['PM25'].agg('mean')

fig = px.bar(gdf, x='Average')






app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Example web application framework for SatPM data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure= fig
    )
])


if __name__ == '__main__':
    app.run(debug=True)