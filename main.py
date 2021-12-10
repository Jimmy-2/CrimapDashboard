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
fig2 = px.histogram(df, x='PERP_RACE', nbins=20)
fig3 = px.histogram(df, x='PERP_SEX', nbins=20)
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
                children="Crimap Dashboard", className="header-title"
            ),
            html.H2(
                children="NYPD Arrest Data (Year to Date)", className="header-subtitle"
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
                html.Div([
                    dcc.Graph(figure=fig3)

                ],
                    style={'width': '49%', 'display': 'inline-block'}),

                html.Div([

                    dcc.Graph(figure=fig2)
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})

            ]),

            html.Div([
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    page_size=15
                ),

            ]),




        ]),
        dcc.Tab(

            label='Map', children=[

            ]),

    ]),




])


@app.callback(
    Output('graph1', 'figure'),
    [Input('dropdown1', 'value')]
)
# graph plot and styling
def update_graph(value):
    if value == 'cus':
        xx = ['North indian', 'chinese', 'continental', 'cafe', 'fast food', 'south indian', 'italian', 'desserts',
              'biryani', 'beverages']
        y1 = x1
        col = 'lightcoral'
    if value == 'dish':
        xx = ['pasta', 'burgers', 'cocktails', 'pizza', 'biryani', 'coffee', 'mocktails', 'sandwiches', 'paratha',
              'noodles']
        y1 = s1
        col = 'skyblue'
    return {'data': [go.Bar(
        x=xx,
        y=y1,
        marker_color=col),

    ],
        'layout': go.Layout(
            title='Top 10 cuisines',
            plot_bgcolor='#26332a',
            paper_bgcolor='#26332a',
            xaxis_tickangle=-17,

            xaxis=dict(
                # type='line',
                title='Most liked dish',
                showgrid=True,
                showline=True,
                color='white',
                linewidth=1,

            ),
            yaxis=dict(
                title='Count',
                showgrid=True,
                showline=True,
                gridcolor='#bdbdbd',
                color='white',
                linewidth=1
            ),
            margin={'l': 60, 'b': 40, 't': 30, 'r': 60},
            # legend={'x': 0.5, 'y': 1},
            hovermode='closest',

        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
