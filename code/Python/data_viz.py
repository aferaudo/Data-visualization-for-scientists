from urllib.request import urlopen
import pandas as pd
import json
import plotly.express as px
import geopandas as gpd
import plotly.io as pio

# Dati Arpae rifiuti per comuni
# https://dati.arpae.it/dataset/rifiuti-urbani-per-comune/resource/36565db6-3242-4444-8b16-c0f6128e4dc9

# Dati geojson confini comuni emilia romagna
# https://github.com/openpolis/geojson-italy/blob/master/geojson/limits_R_8_municipalities.geojson

def main():
    
    df = pd.read_csv("data/EmiliaRomagna.csv",  dtype={"COMUNE": str})
    df_RD = pd.DataFrame()
    df_RD["name"] = df["COMUNE"]
    df_RD["RD"] = df["RD(%)"].str.rstrip('%').astype('float')
    
    # print(df_RD)
    with urlopen("https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_R_8_municipalities.geojson") as response:
        municipalities = json.load(response)
        # print(municipalities)
        fig = px.choropleth_mapbox(df_RD, geojson=municipalities, locations=df_RD.name, color = df_RD.RD,
        featureidkey="properties.name",
        color_continuous_scale = ["gold", "green"],
        range_color=(20, 100),
        mapbox_style="carto-positron",
        zoom=8, center = {"lat": 44.586717, "lon": 11.051426},
        opacity=0.5,
        labels={"RD": "Recycling percentage"})
        fig.update_geos(showsubunits=False)
        fig.update_layout(height = 1000,
                  width = 1700,font_family="Calibri", font_size=12, margin={"r":0,"t":0,"l":0,"b":0})
       
       # export as static image
        pio.write_image(fig, "er.png", scale=8)
        fig.show()


if __name__ == '__main__':

    main()