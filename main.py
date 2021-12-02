import pandas as pd
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)
server = app.server

#---------------------------------------------------------------
#Taken from https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases
df = pd.read_csv("NYPD_Arrest_Data__Year_to_Date_.csv")

dff = df.groupby('ARREST_PRECINCT', as_index=False)[['PERP_SEX','PERP_RACE']].sum()
print (dff[:5])
pie = px.pie(df, names='PERP_SEX', )
pie.update_layout(paper_bgcolor="plum")

pie2 = px.pie(df, names='PERP_RACE')
pie2.update_layout(paper_bgcolor="powderblue")
fig = go.Figure()
#---------------------------------------------------------------
app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
app.layout = html.Div([
    html.Div(
        children=[

            html.H1(
                children="NYPD Arrest Data (Year to Date)", className="header-title"
            ),

        ],
        className="header",
    ),
    dcc.Tabs([
        dcc.Tab(label='Graphs and Charts', children=[
            html.Div([
                html.Div([
                    dcc.Graph(figure=pie),
                ],
                    style={'width': '49%', 'display': 'inline-block'}),

                html.Div([

                    dcc.Graph(figure=pie2),
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})

            ]),

            html.Div([



            ], style={
                'padding': '10px 5px'
            }),

            dcc.Graph(
                figure=fig,
                id='crossfilter-indicator-scatter',
                hoverData={'points': [{'customdata': 'shot'}]}

            )

        ]),
        dcc.Tab(

            label='Map', children=[

            ]),

    ]),




])


if __name__ == '__main__':
    app.run_server(debug=True)
