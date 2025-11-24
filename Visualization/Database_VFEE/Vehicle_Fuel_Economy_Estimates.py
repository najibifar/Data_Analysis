from pathlib import Path
import pandas as pd
import os

from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px

app = Dash(__name__)

styles = {"pre" :{"border":"thin lightgrey solid", "overflowX":"scroll"}}

#sr_file = os.path.join("data", "raw", "Vehicle Fuel Economy Estimates.csv")
df = pd.read_csv("Vehicle Fuel Economy Estimates.csv")

min_year = df["Year"].min()
max_year = df["Year"].max()
all_years = df["Year"].unique()
transmission_types = df["Transmission"].unique()


data_table_cols = [
    "Make",
    "Model",
    "Year",
    "Transmission",
    "Drive",
    "Class",
    "Engine Cylinders",
    "Engine Displacement",
    "Fuel Type",
]

total_clicks = 0

app.layout = html.Div(
    [
        html.H1("Fuel Analysis"),
        html.Div([
            html.P("Talk Python Training Example"),
            dcc.Graph(id="histogram-with-slider", config={"displayModeBar": False}),
            dcc.Graph(id="scatter-plot"),
            html.Label("Year Range"),
            dcc.RangeSlider(
                id="year-slider",
                min=min_year,
                max=max_year,
                value=(min_year,max_year),
                marks={str(Year):str(Year) for Year in all_years},
            ),
            html.Label("Transmission Type"),
            dcc.Checklist(
                id="transmission-list",
                options=[{
                    "label":i,
                    "value":i
                } for i in transmission_types],
                value=transmission_types,
                labelStyle={"display":"inline-block"},
            ),
            html.Hr(),
            html.Button("Reset selections", id="reset", n_clicks=0),
            html.H3(id="selected_count"),
            dash_table.DataTable(
                id="data-table",
                data=[],
                page_size=10,
                columns=[{
                    "name":i,
                    "id":i
                }for i in data_table_cols],
            ),
        ]),
    ],
    style={"margin-bottom":"150px"},
)

@app.callback
