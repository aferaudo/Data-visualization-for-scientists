from urllib.request import urlopen
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import plotly.io as pio

# Dati Arpae rifiuti per comuni
# https://dati.arpae.it/dataset/rifiuti-urbani-per-comune/resource/36565db6-3242-4444-8b16-c0f6128e4dc9

# Dati geojson confini comuni emilia romagna
# https://github.com/openpolis/geojson-italy/blob/master/geojson/limits_R_8_municipalities.geojson

def main():
    
    df = pd.read_csv("data/EmiliaRomagna.csv",  dtype={"COMUNE": str})
        
    # barchart dataframe production
    df_bo = pd.DataFrame()
    df_bo = df[df["COMUNE"] == "Bologna"].reset_index()
    df_bo = df_bo[["anno","RD(kg)","RI(kg)","RU(kg)"]]

    print("Building bar chart...")
    # barchart building
    fig_bar = go.Figure()

    # first bar: RD(KG)
    fig_bar.add_trace(go.Bar(
        x = df_bo["anno"],
        y = df_bo["RD(kg)"],
        name = "Recycled waste",
        marker_color = "rgb(102,194,165)",
        # marker_line_width=1.5,
        # marker_line_color="black"
    ))

     # second bar: RI(KG)
    fig_bar.add_trace(go.Bar(
        x = df_bo["anno"],
        y = df_bo["RI(kg)"],
        name = "Non-recyclable waste",
        marker_color = "rgb(252,141,98)",
        # marker_line_width=1.5,
        # marker_line_color="black"
    ))

    # Third bar: RU(KG)
    fig_bar.add_trace(go.Bar(
        x = df_bo["anno"],
        y = df_bo["RU(kg)"],
        name = "Total Urban waste",
        marker_color = "rgb(141,160,203)",
        # marker_line_width=1.5,
        # marker_line_color="black"
    ))

    fig_bar.update_layout(barmode='group', 
        bargap=0.2,  
        plot_bgcolor='rgba(0,0,0,0)',
         font=dict(
            family="Times New Roman, monospace",
            size=14,
            color="black"
        ),
        # legend=dict(
        #     yanchor="top",
        #     y=0.99,
        #     xanchor="left",
        #     x=0.01
        # )
    )
    fig_bar.update_yaxes(title="Waste (kg)", 
        showline=True, 
        linecolor="black",
        showgrid=True, 
        gridcolor="black",
        )
    fig_bar.update_xaxes(title="Year", 
        showline=True, 
        linecolor="black", 
        showgrid=False,
        )
    fig_bar.show()
    pio.write_image(fig_bar,"../../graphs/barChart.pdf")
    print("done")

    print("Building choropleth map...")
    df = df[df["anno"] == 2020]
    df_RD = pd.DataFrame()
    df_RD["name"] = df["COMUNE"]
    df_RD["RD"] = df["RD(%)"].str.rstrip('%').astype('float')
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
        pio.write_image(fig, "../../graphs/er.pdf", scale=8)
        fig.show()
    print("done")

if __name__ == '__main__':

    main()