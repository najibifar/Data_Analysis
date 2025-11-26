from pathlib import Path
import pandas as pd
import os

from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px

app = Dash(__name__)

styles = {"pre" :{"border":"thin lightgrey solid", "overflowX":"scroll"}}

#sr_file = os.path.join("data", "raw", "Vehicle Fuel Economy Estimates.csv")
df = pd.read_csv("Vehicle Fuel Economy Estimates.csv", low_memory=False)

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

@app.callback(
    Output("histogram-with-slider", "figure"),
    Output("scatter-plot", "figure"),
    Output("data-table", "data"),
    Output("selected_count", "children"),
    Input("year-slider", "value"),
    Input("transmission-list", "value"),
    Input("scatter-plot", "selectedData"),
    Input("reset", "n_clicks"),
)
def update_figure(year_range, transmission_list, selectedData, n_clicks):
    # فیلتر اولیه بر اساس سال و گیربکس
    filtered_df = df[
        (df["Year"] >= year_range[0]) &
        (df["Year"] <= year_range[1]) &
        (df["Transmission"].isin(transmission_list))
    ].copy()

    # هیستوگرام: هزینه سالانه سوخت
    fig_hist = px.histogram(
        filtered_df,
        x="Annual Fuel Cost (FT1)",
        color="Class",
        labels={"Annual Fuel Cost (FT1)": "Annual Fuel Cost ($)"},
        nbins=40,
    )

    fig_scatter = px.scatter(
        filtered_df,
        x="Engine Displacement",
        y="Annual Fuel Cost (FT1)",
        hover_name="Model",
        hover_data=["Make", "Year", "Transmission", "Class"],
        custom_data=filtered_df.index,  # برای بازیابی ایندکس اصلی
    )
    fig_scatter.update_layout(clickmode="event+select")
    fig_scatter.update_traces(
        marker=dict(color="steelblue"),
        selected_marker=dict(color="red")
    )

    # منطق Reset: اگر دکمه زده شده، انتخاب را پاک کن
    if n_clicks > 0:
        selectedData = None

    # اعمال انتخاب (اگر وجود داشت)
    if selectedData and "points" in selectedData:
        indices = [point["customdata"] for point in selectedData["points"]]
        final_df = df.loc[indices]
        label = f"Showing {len(indices)} selected vehicles"
    else:
        # در غیر این‌صورت، 10 ردیف اول جدول را نشان بده
        final_df = filtered_df.head(10)
        total_count = len(filtered_df)
        label = f"No points selected – showing first {len(final_df)} of {total_count} vehicles"

    # مطمئن شو که فقط ستون‌های جدول را برگردانی
    table_data = final_df[data_table_cols].to_dict("records")

    return fig_hist, fig_scatter, table_data, label
          
